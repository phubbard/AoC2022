# https://adventofcode.com/2022/day/1

"""
p-code it
for every line of input
    if blank or EOF
        emit running sum as elf N
    else
        sum += int(line)

output is array of caloric sums? why not, only search once

Sample data
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000

winner is elf 4 at 24000
"""

test_data = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

DATAFILE = './data/1.txt'
data = open(DATAFILE, 'r').readlines()


def compute_totals(data):
    elves = []
    sum = 0
    for item in data:
        if len(item.strip()) == 0:
            elves.append(sum)
            sum = 0
        else:
            cur_val = int(item)
            sum = sum + cur_val

    return elves


def report_highest(elves):
    max = 0
    index = -1

    for idx, value in enumerate(elves):
        if value > max:
            index = idx
            max = value

    print(f'Max value {max} held by elf {index}')


def top_three(elves):
    elves.sort()
    elves.reverse()
    return elves[0:3]


if __name__ == '__main__':
    elves = compute_totals(test_data.split('\n'))
    report_highest(elves)

    elves = compute_totals(data)
    report_highest(elves)

    top = top_three(elves)
    print(top)
    print(sum(top))