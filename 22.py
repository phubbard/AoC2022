import re
import numpy as np

sample= """
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

10R5L5R10L4R5L5"""

DATAFILE = "./data/22.txt"

# NB - ends with missing direction - see parser for special case handling
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
    # The heavy lifting only takes one call
    tuples = matcher.findall(move_str)

    # Special case - last two are numbers - full data
    ending_characters = move_str[-2:]
    if move_str[-2].isdigit() and move_str[-1].isdigit():
        tuples.append((ending_characters, None))
    # In sample data, single digit numeric last character
    elif move_str[-1].isdigit():
        tuples.append((move_str[-1], None))
    else:
        print("WARNING no trailing move found in directions")

    # Validate and convert to ints
    rc = []
    for idx, value in enumerate(tuples):
        try:
            temp = int(value[0])
            rc.append((temp, value[1],))
        except:
            print(f'Error parsing {value=} at {idx=}')

    return rc


def find_start(map):
    # Return row, col for the starting point - leftmost top edge
    row = 0
    for col in range(map.shape[1]):
        if map[row][col] == OPEN:
            return row, col, 'R'

    return None, None


def find_open(game_map, row, col, facing):
    # if we're moving right and need the next open cell, its on the left edge
    # N.B. Only called for wraparound.
    # Returns row, col or None if wall
    match facing:
        case 'L':
            for idx in range(game_map.shape[1] - 1, col, -1):
                if game_map[row][idx] == OPEN:
                    return row, idx
                if game_map[row][idx] == WALL:
                    return
        case 'R':
            # Start from left edge, skipping nulls
            for idx in range(col):
                if game_map[row][idx] == OPEN:
                    return row, idx
                if game_map[row][idx] == WALL:
                    return
        case 'U':
            for idx in range(game_map.shape[0] - 1, 0, -1):
                if game_map[idx][col] == OPEN:
                    return idx, col
                if game_map[idx][col] == WALL:
                    return
        case 'D':
            for idx in range(row):
                if game_map[idx][col] == OPEN:
                    return idx, col
                if game_map[idx][col] == WALL:
                    return


def new_direction(facing, rotation):
    dd = 'LURD'
    old_idx = dd.index(facing)
    if rotation == 'R':
        new_idx = (old_idx + 1) % len(dd)
    else:
        new_idx = (old_idx - 1) % len(dd)
    return dd[new_idx]


def test_new_direction():
    assert new_direction('D', 'L') == 'R'
    assert new_direction('D', 'R') == 'L'
    assert new_direction('L', 'L') == 'D'
    assert new_direction('R', 'L') == 'U'


def calc_password(row, col, facing):
    temp = (1000 * (row + 1)) + (4 * (col + 1))
    match facing:
        case 'L': m = 2
        case 'R': m = 0
        case 'U': m = 3
        case 'D': m = 1
    return temp + m


def test_calc_password():
    assert calc_password(5, 7, 'R') == 6032


def move(facing, count, gs_map, start_row, start_col):
    num_rows = gs_map.shape[0]
    num_cols = gs_map.shape[1]
    move_count = 0
    end_reason = None

    new_col = start_col
    new_row = start_row
    for _ in range(int(count)):
        if facing == 'L' or facing == 'R':
            increment = 1 if facing == 'R' else -1
            temp = new_col
            new_col = (new_col + increment) % num_cols
            if gs_map[new_row][new_col] == OPEN:
                move_count += 1
                continue
            if gs_map[new_row][new_col] == WALL:
                new_col = temp
                end_reason = 'Wall'
                break
            if gs_map[new_row][new_col] == NULL:
                rc = find_open(gs_map, new_row, temp, facing)
                if not rc:
                    new_col = temp
                    end_reason = 'Wall'
                    break
                else:
                    new_col = rc[1]
                    move_count += 1
                    continue

        if facing == 'D' or facing == 'U':
            increment = 1 if facing == 'D' else -1
            temp = new_row
            new_row = (new_row + increment) % num_rows
            if gs_map[new_row][new_col] == OPEN:
                move_count += 1
                continue
            if gs_map[new_row][new_col] == WALL:
                new_row = temp
                end_reason = 'Wall'
                break
            if gs_map[new_row][new_col] == NULL:
                rc = find_open(gs_map, temp, new_col, facing)
                if not rc:
                    new_row = temp
                    end_reason = 'Wall'
                    break
                new_row = rc[0]
                move_count += 1
                continue
    if move_count != count:
        print(f"{move_count} {facing} out of {count} moves, {end_reason=}")
    else:
        print(f'Moved {count} {facing}')
    return new_row, new_col


if __name__ == '__main__':
    if True:
        tokens = sample.split('\n\n')
    else:
        tokens = open(DATAFILE).read().split('\n\n')

    game_map = parse_map(clean_data_lines(tokens[0].split(('\n'))))
    directions = parse_directions(tokens[1].strip())
    row, col, facing = find_start(game_map)
    for step in directions:
        print(f"Starting {row=} {col=} {facing=} {step=}")
        row, col = move(facing, step[0], game_map, row, col)
        if step[1]:
            facing = new_direction(facing, step[1])

    print(f"{calc_password(row, col, facing)=} {row=} {col=} {len(directions)=}")