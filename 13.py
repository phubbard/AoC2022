import copy
import json
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(message)s')
log = logging.getLogger()

# Problem spec https://adventofcode.com/2022/day/13
DATAFILE = "./data/13.txt"

sample_data = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""

sample_answers = [True, True, False, True, False, True, False, False]


def is_list(item) -> bool:
    return type(item) == list



def string_to_native(string_value):
    eval_answer = eval(string_value)
    json_answer = json.loads(string_value)
    if eval_answer != json_answer:
        raise Exception(f"MISMATCH ghiven -> {string_value}\n  eval -> {eval_answer}\n  json -> {json_answer}")
    return json_answer



def compare_lists(left, right, depth):
    log.debug(f"{depth * '  '} - Compare {left} vs {right}")
    # True if correct order, false if wrong, None if we cannot decide.
    assert is_list(left) and is_list(right)

    idx = 0
    for idx, left_value in enumerate(left):
        if idx >= len(right):
            log.debug(f"{depth * '  '} - Right side ran out of items, so inputs are not in the right order")
            return False
        rc = compare_pair(left_value, right[idx], depth)
        if rc is None:
            continue
        else:
            # The pair comparison returned a definite answer - we're done
            return rc
    else: 
        if idx + 1 < len(right):
            log.debug(f"{depth * '  '} - Left side ran out of items, so inputs are in the right order")
            return True

    return None


def compare_lists_outer(left, right):
    depth = 0
    rc = compare_lists(left, right, depth)
    if rc is None:
        log.debug(f"{depth * '  '} - !!! Left side ran out of items, so inputs are in the right order")

        return True
    return rc


def compare_pair(left, right, depth):
    log.debug(f"{depth * '  '} - Compare {left} vs {right}")
    # Returns true if in correct order, false if wrong order, None if undecidable
    if (not is_list(left)) and (not is_list(right)):
        if left < right:
            log.debug(f"{depth * '  '} - Left side is smaller, so inputs are in the right order")
            return True
        if right < left:
            log.debug(f"{depth * '  '} - Right side is smaller, so inputs are not in the right order")
            return False
        # They're equal - continue
        return None

    left  = left  if is_list(left)  else [left]
    right = right if is_list(right) else [right]

    return compare_lists(left, right, depth + 1)


class Reception:
    def __init__(self, indx, left, right):
        self.RECEPTION_INDEX = indx
        self.RECEPTION_LEFT  = string_to_native(left)
        self.RECEPTION_RIGHT = string_to_native(right)

    def __str__(self):
        rv = ""
        rv += f"\n  pair -> index: {self.RECEPTION_INDEX}"
        rv += f"\n           left: {self.RECEPTION_LEFT}"
        rv += f"\n          right: {self.RECEPTION_RIGHT}"
        return rv

    def as_input_file_string(self):
        left  = str(self.RECEPTION_LEFT)  .replace(" ", "")
        right = str(self.RECEPTION_RIGHT) .replace(" ", "")
        return f"{left}\n{right}"


class Dataset:
    def __init__(self, reception_list):
        self.DATASET_TUPLE = tuple(reception_list)

    def __str__(self):
        rv = "<<DATASET"
        for idx, reception in enumerate(self.DATASET_TUPLE):
            rv += str(reception)
        rv += "\n>>"
        return rv

    def dump_to(self, filename):
        next_string = None
        with open(filename, 'w') as file:
            for reception in self.DATASET_TUPLE:
                if next_string is not None: file.write("\n\n")
                next_string = reception.as_input_file_string()
                file.write(next_string)

#
INPUTS_IN_RIGHT_ORDER     = 1
INPUTS_NOT_IN_RIGHT_ORDER = 2
INPUTS_ARE_SAME           = 3

def is_integer(value): return type(value) == int
def is_list(value):    return type(value) == list

def compare_values_inner(left_value, right_value, depth):
    inner_depth = depth + 2

    if False: pass

    elif is_integer(left_value) and is_integer(right_value):
        if False: pass
        elif left_value < right_value: return INPUTS_IN_RIGHT_ORDER
        elif left_value > right_value: return INPUTS_NOT_IN_RIGHT_ORDER
        else:                          return INPUTS_ARE_SAME

    elif is_list(left_value) and is_list(right_value):
        while True:
            left_list_is_empty  = len(left_value)  == 0
            right_list_is_empty = len(right_value) == 0
            if False: pass
            elif left_list_is_empty and right_list_is_empty: return INPUTS_ARE_SAME
            elif left_list_is_empty:                         return INPUTS_IN_RIGHT_ORDER
            elif right_list_is_empty:                        return INPUTS_NOT_IN_RIGHT_ORDER
            else:
                # Both lists have at least one: pop first of each
                left_list_first  = left_value.pop(0)
                right_list_first = right_value.pop(0)
                sub_check = compare_values_inner(left_list_first, right_list_first, inner_depth)
                if sub_check in {INPUTS_IN_RIGHT_ORDER, INPUTS_NOT_IN_RIGHT_ORDER}: return sub_check

    elif is_integer(left_value) and is_list(right_value):
        return compare_values_inner([left_value], right_value, inner_depth)
        
    elif is_list(left_value) and is_integer(right_value):
        return compare_values_inner(left_value, [right_value], inner_depth)

    else:
        raise Exception("Unexpected, and most unfortunate")


def compare_values_outer_brad(left, right):
    rc = compare_values_inner(left, right, 0)

    if False: pass
    elif rc == INPUTS_IN_RIGHT_ORDER:     return True
    elif rc == INPUTS_NOT_IN_RIGHT_ORDER: return False
    else:  raise Exception("Grievious injury indeed")


def parse_input(data_lines):

    groupings = data_lines.strip().split("\n\n")

    raw_receptions = []

    for grouping in groupings:
        split_grouping = grouping.split("\n")
        split_length = len(split_grouping)
        if split_length != 2:
            raise Exception(f"Malformed grouping with split_length:{split_length} --> {grouping}")
        raw_receptions.append(Reception(len(raw_receptions) + 1, split_grouping[0], split_grouping[1], ))
    return Dataset(raw_receptions)


if __name__ == '__main__':
    log.info("Beginning parse...")
    if False:
        dataset = parse_input(sample_data)
        dataset.dump_to("regurgitate-13-sample.txt")
    else:
        dataset = parse_input(open(DATAFILE, 'r').read())
        dataset.dump_to("regurgitate-13-datafile.txt")

    if False:
        log.info("Showing read tuples...")
        log.info(str(dataset))
    else:
        log.info("Show tuples suppressed.")

    running_sum_of_ordered_pairs = 0
    for idx, reception in enumerate(dataset.DATASET_TUPLE):
        log.info(f" == Pair {reception.RECEPTION_INDEX} ==")
        old_result = compare_lists_outer       (reception.RECEPTION_LEFT, reception.RECEPTION_RIGHT)
        new_result = compare_values_outer_brad (reception.RECEPTION_LEFT, reception.RECEPTION_RIGHT)
        log.info(f"")
        if old_result != new_result:
            pass # raise Exception(f"old_result:{old_result} != new_result:{new_result}")
        if new_result:
            running_sum_of_ordered_pairs += reception.RECEPTION_INDEX
        log.info(f" Index:{reception.RECEPTION_INDEX:02} END")
    log.info(f"\nSum of indices is {running_sum_of_ordered_pairs}")

    log.info(f"Last official run emitted correct answer -> Sum of indices is 6046.")
