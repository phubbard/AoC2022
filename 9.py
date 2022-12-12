from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from math import sqrt

test_data = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
test_visited = 13
DATAFILE = "./data/9.txt"
step_two_test_data = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""
step_two_visited = 36
Move = Enum('Move', ['UL', 'U', 'UR', 'L', 'NOOP', 'R', 'LD', 'D', 'DR'])


@dataclass
class Point:
    row: int = 0
    col: int = 0


def str_to_move(move_str: str) -> Move:
    # Is there a clever way to do this?
    match move_str:
        case 'L':
            return Move.L
        case 'R':
            return Move.R
        case 'U':
            return Move.U
        case 'D':
            return Move.D


def do_move(begin: Point, direction: Move) -> Point:
    end = deepcopy(begin)
    match direction:
        case Move.UL:
            end.row += 1
            end.col -= 1
        case Move.U:
            end.row += 1
        case Move.UR:
            end.row += 1
            end.col += 1
        case Move.L:
            end.col -= 1
        case Move.NOOP:
            pass
        case Move.R:
            end.col += 1
        case Move.LD:
            end.row -= 1
            end.col -= 1
        case Move.D:
            end.row -= 1
        case Move.DR:
            end.row -= 1
            end.col += 1
    return end


def move_needed(head: Point, tail: Point) -> bool:
    max_dist = sqrt(2.0)
    dist_squared = (head.row - tail.row) ** 2 + (head.col - tail.col) ** 2
    dist = sqrt(dist_squared)
    return dist > max_dist


def decide_move(head, tail) -> Move:
    if not move_needed(head, tail):
        return Move.NOOP

    move_up = head.row > tail.row
    move_down = head.row < tail.row
    move_right = head.col > tail.col
    move_left = head.col < tail.col
    if move_left and move_up:
        return Move.UL
    if move_up and move_right:
        return Move.UR
    if move_up:
        return Move.U
    if move_left and move_down:
        return Move.LD
    if move_right and move_down:
        return Move.DR
    if move_down:
        return Move.D
    if move_left:
        return Move.L
    if move_right:
        return Move.R
    print(f"warning - no op move from {head} to {tail}")
    return Move.NOOP


def test_mn():
    head = Point(0, 0)
    tail = Point(0, 1)
    assert move_needed(head, tail) == False
    assert move_needed(tail, head) == False
    assert move_needed(head, head) == False
    tail = Point(1, 1)
    assert move_needed(head, tail) == False
    head = Point(3, 3)
    assert move_needed(head, tail) == True
    assert move_needed(tail, head) == True


def test_move():
    start = Point(0, 0)
    end = do_move(start, Move.UR)
    assert end == Point(1, 1)
    assert do_move(start, Move.NOOP) == start
    assert do_move(start, Move.UR) != start
    assert do_move(end, Move.LD) == start


def test_decide_move():
    head = Point(3, 3)
    tail = Point(2, 3)
    move = decide_move(head, tail)
    assert move == Move.NOOP
    tail = Point(1, 3)
    move = decide_move(head, tail)
    assert move == Move.U

    tail = Point(4, 4)
    assert decide_move(head, tail) == Move.NOOP
    tail = Point(5, 5)
    assert decide_move(head, tail) == Move.LD


def run_data(data_lines):
    head = Point(0, 0)
    tail = Point(0, 0)
    saved_tailpath = set()

    for line in data_lines:
        if len(line) == 0:
            continue

        tokens = line.strip().split(' ')

        string = tokens[0]
        reps = tokens[1]
        # e.g. R 5
        for idx in range(int(reps)):
            move = str_to_move(string)
            head = do_move(head, move)
            correction = decide_move(head, tail)
            tail = do_move(tail, correction)
            saved_tailpath.add((tail.row, tail.col,))

    visited = len(saved_tailpath)
    print(f'{visited} visited')


def visualize_tailpath(tailpath: set):
    min_row = min([x[0] for x in tailpath])
    max_row = max([x[0] for x in tailpath])
    min_col = min([x[1] for x in tailpath])
    max_col = max([x[1] for x in tailpath])
    num_rows = max_row - min_row
    num_cols = max_col - min_col

    for row in range(max_row, min_row - 1, -1):
        rc = ''
        for col in range(min_col, max_col + 1):
            if (row, col,) in tailpath:
                rc += '#'
            else:
                rc += '.'
        print(rc)


def run_step_two(data_lines):
    knots = [Point(0, 0) for _ in range(10)]
    saved_tailpath = set()

    for line in data_lines:
        if len(line) == 0:
            continue

        tokens = line.strip().split(' ')
        string = tokens[0]
        move = str_to_move(string)
        reps = int(tokens[1])

        for idx in range(reps):
            knots[0] = do_move(knots[0], move)
            for knot_idx in range(9):
                correction = decide_move(knots[knot_idx], knots[knot_idx + 1])
                knots[knot_idx + 1] = do_move(knots[knot_idx + 1], correction)
            correction = decide_move(knots[8], knots[9])
            knots[9] = do_move(knots[9], correction)
            saved_tailpath.add((knots[9].row, knots[9].col,))

    print(f'Step two {len(saved_tailpath)}')
    visualize_tailpath(saved_tailpath)


if __name__ == '__main__':
    # test_mn()
    # test_move()
    # test_decide_move()
    # run_data(test_data.split('\n'))
    # run_data(open(DATAFILE, 'r'))
    # run_step_two(test_data.split('\n'))
    # run_step_two(step_two_test_data.split('\n'))
    run_step_two(open(DATAFILE, 'r'))