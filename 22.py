import numpy as np
import re

sample_map="""
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.
"""
sample_moves = '10R5L5R10L4R5L5'
# FIXME - ends with missing direction
pattern = r'(\d+)(\w)'
matcher = re.compile(pattern)

OPEN = 1
WALL = 2
NULL = 0

def arrays(row, column, fill=0):
    # Create and allocate a 2D array. Copypasta from SO with edits.
    return [[fill]*column for i in range(row)]


def clean_data_lines(data_lines):
    # Blank lines throw off the parsing and indexing
    return [x for x in data_lines if len(x) > 0]


def parse_map(data_lines):
    num_rows = len(data_lines)
    num_cols = max([len(x) for x in data_lines])
    rc = arrays(num_rows, num_cols)
    # rc = np.zeros((num_rows, num_cols), dtype=np.int16)

    for row_idx, row in enumerate(data_lines):
        if len(row) == 0:
            continue
        for col_idx, char in enumerate(row):
            temp = None
            if char == ' ':
                temp = NULL
            elif char == '.':
                temp = OPEN
            elif char == '#':
                temp = WALL
            rc[row_idx][col_idx] = temp
    return np.array(rc)


def parse_directions(move_str):
    # Return a vector of (direction, count) tuples
    return matcher.findall(move_str)


def find_start(map):
    # Return row, col for the starting point - leftmost top edge
    row = 0
    for col in range(map.shape[1]):
        if map[row][col] == OPEN:
            return row, col

    return None, None


def move(direction, count, map, start_row, start_col):
    num_rows = map.shape[0]
    num_cols = map.shape[1]
    moves = []

    for _ in range(count):
        match direction:
            case 'L':
                new_row = (start_col - 1) % num_cols

            case 'R':
            case 'U':
            case 'D':


if __name__ == '__main__':
    game_map = parse_map(clean_data_lines(sample_map.split(('\n'))))
    directions = parse_directions(sample_moves)
    row, col = find_start(game_map)
    for step in directions:
        row, col = move(step[0], step[1], game_map, row, col)

    print(f"{row=} {col=} {len(directions)=}")