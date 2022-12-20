
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


class Dataset:
    def __init__(self, reception_list):
        self.DATASET_TUPLE = tuple(reception_list)

    def __str__(self):
        rv = "<<DATASET"
        for idx, reception in enumerate(self.DATASET_TUPLE):
            rv += str(reception)
        rv += "\n>>"
        return rv


def parse_input(data_lines):

    groupings = data_lines.strip().split("\n\n")

    raw_receptions = []

    for grouping in groupings:
        split_grouping = grouping.split("\n")
        split_length = len(split_grouping)
        for idx, sting in enumerate(split_grouping):
            log.info(f"DEBUG: idx:{idx} -> {sting}")
        if split_length != 2:
            raise Exception(f"Malformed grouping with split_length:{split_length} --> {grouping}")
        raw_receptions.append(Reception(len(raw_receptions) + 1, split_grouping[0], split_grouping[1], ))
    return Dataset(raw_receptions)


if __name__ == '__main__':
    log.info("Beginning parse...")
    if True:
        dataset = parse_input(sample_data)
    else:
        dataset = parse_input(open(DATAFILE, 'r').read())

    if True:
        log.info("Showing read tuples...")
        log.info(str(dataset))
    else:
        log.info("Show tuples suppressed.")

    running_sum_of_ordered_pairs = 0
    for idx, reception in enumerate(dataset.DATASET_TUPLE):
        log.info(f" == Pair {reception.RECEPTION_INDEX} ==")
        result = compare_lists_outer(reception.RECEPTION_LEFT, reception.RECEPTION_RIGHT)
        log.info(f" Index:{reception.RECEPTION_INDEX:02} END -> {result}")
        log.info(f"")
        if result:
            running_sum_of_ordered_pairs += reception.RECEPTION_INDEX
    log.info(f"\nSum of indices is {running_sum_of_ordered_pairs}")

    log.info(f"Sum of indices is 5513 from above.")
