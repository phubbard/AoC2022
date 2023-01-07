
"""
This one is much harder. Let's try for some pieces first. We need two parsers
- initial stack into memory
- moves
"""
from collections import deque


DATAFILE = './data/5.txt'
# Rather than writing a parser for this, just manually encode the initial conditions.
COLS = [
    'GDVZJSB',
    'ZSMGVP',
    'CLBSWTQF',
    'HJGWMRVQ',
    'CLSNFMD',
    'RGCD',
    'HGTRJDSQ',
    'PFV',
    'DRSTJ'
]

# Create an array of deques
STACKS = [deque(x) for x in COLS]
TEST_COLS = [
    'ZN',
    'MCD',
    'P'
]
TEST_MOVES = """move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""
TEST_ANSWER = 'CMZ'
P2_ANSWER = 'MCD'


def parse_move(data_line):
    # Could use regex but overkill
    tokens = data_line.strip().split(' ')
    assert tokens[0] == 'move'
    count = int(tokens[1])
    assert tokens[2] == 'from'
    source = int(tokens[3]) - 1
    assert tokens[4] == 'to'
    dest = int(tokens[5]) - 1
    return count, source, dest


def do_move(count, source, dest, stacks):
    for idx in range(count):
        stacks[dest].append(stacks[source].pop())
    return stacks


def do_9001_move(count, src, dest, stacks):
    elements = []
    for idx in range(count):
        assert len(stacks[src]) > 0
        elements.append(stacks[src].pop())

    elements.reverse()
    stacks[dest].extend(elements)
    pass


def get_tops(stacks):
    rc = ''
    for col in stacks:
        rc += col.pop()
    return rc


def test_step_one():
    stacks = [deque(x) for x in TEST_COLS]
    for move in TEST_MOVES.split('\n'):
        if len(move) == 0:
            continue

        count, src, dest = parse_move(move)
        do_move(count, src, dest, stacks)

    rc = get_tops(stacks)
    assert rc == TEST_ANSWER


def test_step_two():
    stacks = [deque(x) for x in TEST_COLS]
    for move in TEST_MOVES.split('\n'):
        if len(move) == 0:
            continue

        count, src, dest = parse_move(move)
        do_9001_move(count, src, dest, stacks)

    rc = get_tops(stacks)
    assert rc == P2_ANSWER


def steps():
    # Need two copies as the moves are in-place
    stacks = [deque(x) for x in COLS]
    v2_stacks = [deque(x) for x in COLS]

    data_lines = open(DATAFILE, 'r').readlines()
    # Skip over initial state and blank lines
    for line in data_lines[10:]:
        count, src, dest = parse_move(line)
        do_move(count, src, dest, stacks)
        do_9001_move(count, src, dest, v2_stacks)
    rc = get_tops(stacks)
    rc2 = get_tops(v2_stacks)
    print(f'{rc} v1 {rc2} v2')

if __name__ == '__main__':
    test_step_one()
    test_step_two()
    steps()
