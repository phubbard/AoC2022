
import logging

DATAFILE = './data/13.txt'

logging.basicConfig(level=logging.DEBUG, format='%(pathname)s(%(lineno)s): %(levelname)s %(message)s')
log = logging.getLogger()

# Problem spec https://adventofcode.com/2022/day/13
DATAFILE = "./data/13.txt"

sample_data = """[1,1,3,1,1]
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
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

sample_answers = [True, True, False, True, False, True, False, False]


def is_list(item:str) -> bool:
    # TODO verify that this suffices!
    return not item.isnumeric()


def compare_lists(left, right):
    # True if correct order, false if wrong, None if we cannot decide.
    assert is_list(left) and is_list(right)
    left_longer = len(left) > len(right)
    if not left_longer:
        for idx, value in enumerate(left):
            rc = compare_pair(value, right[idx])
            if rc is None:
                continue
            # The pair comparison returned a definite answer - we're done
            return rc
        # We've walked the left list and exhausted the right list.
        return True
    # Left is longer
    for idx, value in enumerate(right):
        rc = compare_pair(left[idx], right)
        if rc is None:
            continue
        return rc
    return False


def compare_pair(left, right):
    log.debug("here we go")
    # Returns true if in correct order, false if wrong order, None if undecidable
    if left.isnumeric() and right.isnumeric():
        if int(left) < int(right):
            return True
        if int(right) > int(left):
            return False
        # They're equal - continue
        return None
    if is_list(left) and is_list(right):
        # TODO pairwise compare with rules about shorter list as per doc
        pass
    if left.isnumeric() and is_list(right):
        return compare_pair([left], right)
    if is_list(left) and right.isnumeric():
        return compare_pair(left, [right])


class Reception:
    def __init__(self, indx, left, right):
        self.RECEPTION_INDEX = indx
        self.RECEPTION_LEFT  = left
        self.RECEPTION_RIGHT = right


class Dataset:
    def __init__(self, reception_list):
        self.DATASET_TUPLE = tuple(reception_list)

    def __str__(self):
        rv = "<<DATASET"
        for idx, reception in enumerate(self.DATASET_TUPLE):
            rv += f"\n  pair {idx:02} -> index: {reception.RECEPTION_INDEX}"
            rv += f"\n              left: {reception.RECEPTION_LEFT}"
            rv += f"\n             right: {reception.RECEPTION_RIGHT}"
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


    row_idx = 0
    for line in data_lines:
        if len(line) == 0:
            continue

        elevation_map.append([])
        col_idx = 0
        for cell in line:
            if cell == 'S':
                    start = (row_idx, col_idx, )
                    elevation_map[row_idx].append(0)
            elif cell == 'E':
                    end = (row_idx, col_idx, )
                    elevation_map[row_idx].append(to_int('z'))
            else:
                    elevation_map[row_idx].append(to_int(cell))
            col_idx += 1
        row_idx += 1

    return start, end, elevation_map


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

