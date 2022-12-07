
test_data = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

test_results = 'pLPvts'
test_scores = [16,38,42,22,20,19]
test_total = 157


two_test_one = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg"""

two_test_two = """wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

two_common = 'Zr'

DATAFILE = './data/3.txt'


def split_line(rs_line):
    assert(len(rs_line) % 2 == 0)
    chars = int(len(rs_line) / 2)
    return rs_line[0: chars], rs_line[chars:]


def find_common(rs_line):
    a, b = split_line(rs_line)
    assert(len(a) == len(b))
    l = set(a)
    r = set(b)
    common = l.intersection(r)
    assert(len(common) == 1)
    cl = list(common)
    return cl[0]


def prioritize(item: str):
    # Lowercase item types a through z have priorities 1 through 26.
    # Uppercase item types A through Z have priorities 27 through 52.
    if item.islower():
        score = (ord(item) - ord('a'))
        score += 1
    else:
        score = (ord(item) - ord('A'))
        score += 27
    return score


def run_packs():
    data_lines = open(DATAFILE, 'r').readlines()
    sum = 0
    for line in data_lines:
        sum += prioritize(find_common(line.strip()))
    print(f"{sum} for {len(data_lines)} lines")


def run_part_two():
    data_lines = open(DATAFILE, 'r').readlines()
    part_two(data_lines)


def part_two(data_lines):
    total = 0
    for x in range(int(len(data_lines) / 3)):
        base = x * 3
        one = set(data_lines[base].strip())
        two = set(data_lines[base + 1].strip())
        three = set(data_lines[base + 2].strip())
        common = one.intersection(two).intersection(three)
        assert(len(common) == 1)
        c_item = list(common)[0]
        total += prioritize(c_item)
        print(f'{c_item} -> {prioritize(c_item)}')

    print(f'Part two total {total}')


def test_part_two():
    data = two_test_one.split('\n')
    part_two(data)

    data = two_test_two.split('\n')
    part_two(data)


def test_algo():
    idx = 0
    for line in test_data.split('\n'):
        if len(line.split()) == 0:
            continue
        print(f"{find_common(line)} should be {test_results[idx]}")
        assert(test_results[idx] == find_common(line))
        idx += 1


def test_prioritizer():
    total = 0
    idx = 0
    for item in test_results:
        priority = prioritize(item)
        total += priority
        assert(test_scores[idx] == priority)
        idx += 1
    assert(total == test_total)
    print('scores matched')


if __name__ == '__main__':
    test_algo()
    test_prioritizer()
    run_packs()
    test_part_two()
    run_part_two()