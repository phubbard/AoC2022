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


def find_open(game_map, row, col, direction):
    # if we're moving right and need the next open cell, its on the left edge
    # TODO What if left edge is a wall?
    match direction:
        case 'L':
            for idx in range(game_map.shape[1] - 1, col, -1):
                if game_map[row][idx] == OPEN:
                    return row, idx
        case 'R':
            for idx in range(col):
                if game_map[row][idx] == OPEN:
                    return row, idx
        case 'U':
            for idx in range(game_map.shape[0], 0, -1):
                if game_map[idx][col] == OPEN:
                    return idx, col
        case 'D':
            for idx in range(row):
                if game_map[idx][col] == OPEN:
                    return idx, col


def move(direction, count, gs_map, start_row, start_col):
    num_rows = gs_map.shape[0]
    num_cols = gs_map.shape[1]
    moves = []

    new_col = start_col
    new_row = start_row
    for _ in range(int(count)):
        if direction == 'L' or direction == 'R':
            increment = 1 if direction == 'R' else -1
            temp = new_col
            new_col = (new_col + increment) % num_cols
            if gs_map[new_row][new_col] == OPEN:
                moves.append(direction)
                continue
            if gs_map[new_row][new_col] == WALL:
                new_col = temp
                break
            if gs_map[new_row][new_col] == NULL:
                rc = find_open(gs_map, new_row, temp, direction)
                if not rc:
                    new_col = temp
                    break
                else:
                    new_col = rc[1]
                    continue

        if direction == 'D' or direction == 'U':
            increment = 1 if direction == 'D' else -1
            temp = new_row
            new_row = (new_row + increment) % num_rows
            if gs_map[new_row][new_col] == OPEN:
                moves.append(direction)
                continue
            if gs_map[new_row][new_col] == WALL:
                new_row = temp
                break
            if gs_map[new_row][new_col] == NULL:
                rc = find_open(gs_map, temp, new_col, direction)
                if not rc:
                    new_row = temp
                    break
                new_row = rc[0]
                continue

    print(f"{moves=} {new_row=} {new_col=}")
    return new_row, new_col


if __name__ == '__main__':
    game_map = parse_map(clean_data_lines(sample_map.split(('\n'))))
    directions = parse_directions(sample_moves)
    row, col = find_start(game_map)
    for step in directions:
        row, col = move(step[1], step[0], game_map, row, col)

    print(f"{row=} {col=} {len(directions)=}")