import pysnooper

test_ranges = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

DATAFILE = './4/input.txt'

def parse_line(data_line):
    ranges = data_line.strip().split(',')
    cr1 = ranges[0].split('-')
    cr2 = ranges[1].split('-')

    r1 = [int(cr1[0]), int(cr1[1])]
    r2 = [int(cr2[0]), int(cr2[1])]

    assert(r1[1] >= r1[0])
    assert(r2[1] >= r2[0])

    return r1, r2


def subset(data_line):
    r1, r2 = parse_line(data_line)

    if r1[1] >= r2[1]:
        if r1[0] <= r2[0]:
            return True

    if r2[1] >= r1[1]:
        if r2[0] <= r1[0]:
            return True

    return False


def in_range(number, range):
    return number >= range[0] and number <= range[1]


def overlap(data_line):
    r1, r2 = parse_line(data_line)

    if in_range(r1[1], r2):
        return True

    if in_range(r2[1], r1):
        return True

    if in_range(r1[0], r2):
        return True

    if in_range(r2[0], r1):
        return True

    return False


def test_data_subset():
    count = 0
    for line in test_ranges.split('\n'):
        if len(line) == 0:
            continue
        if subset(line):
            count += 1
    print(count)


def test_data_overlap():
    count = 0
    for line in test_ranges.split('\n'):
        if len(line) == 0:
            continue
        if overlap(line):
            count += 1
    print(f'{count} overlaps in  test dataset')


def run_steps():
    data_lines = open(DATAFILE, 'r').readlines()
    subset_count = 0
    overlap_count = 0
    for line in data_lines:
        if subset(line):
            subset_count += 1
        if overlap(line):
            overlap_count += 1
    print(f'{subset_count} subsets found, {overlap_count} overlaps out of {len(data_lines)}')



if __name__ == '__main__':
    test_data_subset()
    run_steps()
    test_data_overlap()