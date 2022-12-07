import pysnooper

test_ranges = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""



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


def overlap(data_line):
    r1, r2 = parse_line(data_line)

    if r1[1]


def test_data_subset():
    count = 0
    for line in test_ranges.split('\n'):
        if len(line) == 0:
            continue
        if subset(line):
            count += 1
    print(count)


def run_step_one():
    data_lines = open('./4/input.txt', 'r').readlines()
    count = 0
    for line in data_lines:
        if subset(line):
            count += 1
    print(f'{count} found out of {len(data_lines)}')


if __name__ == '__main__':
    test_data_subset()
    run_step_one()