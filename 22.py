import re
import numpy as np

sample = """
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


def make_2d_array(num_rows, num_cols, fill=0):
    # Create and allocate a 2D array. Copypasta from SO with edits.
    return [[fill] * num_cols for _ in range(num_rows)]


def clean_data_lines(data_lines):
    # Blank lines throw off the parsing and indexing; this drops them
    return [x for x in data_lines if len(x) > 0]


def parse_map(data_lines):
    num_rows = len(data_lines)
    num_cols = max([len(x) for x in data_lines])
    rc = make_2d_array(num_rows, num_cols)
    lookup = {' ': NULL, '.': OPEN, '#': WALL}

    for row_idx, value in enumerate(data_lines):
        for col_idx, char in enumerate(value):
            rc[row_idx][col_idx] = lookup[char]

    return np.array(rc)


def parse_directions(move_str):
    # The heavy lifting only takes one call
    tuples = matcher.findall(move_str)

    # Special case - last two are numbers - full data
    ending_characters = move_str[-2:]
    if move_str[-2].isdigit() and move_str[-1].isdigit():
        assert(move_str[-3].isalpha())
        tuples.append((ending_characters, None))
    # In sample data, single digit numeric last character
    elif move_str[-1].isdigit():
        assert(move_str[-2].isalpha())
        tuples.append((move_str[-1], None))

    # Validate and convert to ints from ascii
    rc = [(int(x[0]), x[1]) for x in tuples]
    return rc


def find_start(game_map):
    # Return row, col for the starting point - leftmost top edge
    starting_row = 0
    for col_idx in range(game_map.shape[1]):
        if game_map[starting_row][col_idx] == OPEN:
            return starting_row, col_idx, 'R'

    assert False


def wrap_around_move(game_map, row, col, facing):
    # if we're moving right and need the next open cell, it's on the left edge. Etc.
    # Returns row, col or None if wall
    start = 0
    loop_step = 1
    if facing in ['L', 'R']:
        if facing == 'L':
            start = game_map.shape[1] - 1
            end = col + 1
            loop_step = -1
        else:  # Rightward
            end = col - 1

        for idx in range(start, end, loop_step):
            if game_map[row][idx] == OPEN:
                return row, idx
            if game_map[row][idx] == WALL:
                return
    else:
        if facing == 'D':
            end = row - 1
        else:  # Upwards
            start = game_map.shape[0] - 1
            end = row + 1
            loop_step = -1

        for idx in range(start, end, loop_step):
            if game_map[idx][col] == OPEN:
                return idx, col
            if game_map[idx][col] == WALL:
                return

    # Guardpost - should be unreachable
    assert False


def new_direction(facing, rotation):
    # Rotation is a barrel shift if array is ordered this way
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
    # their calcs are 1-based, not zero
    fc_add = {'R': 0, 'D': 1, 'L': 2, 'U': 3}
    return (1000 * (row + 1)) + (4 * (col + 1)) + fc_add[facing]


def test_calc_password():
    assert calc_password(5, 7, 'R') == 6032


def move(facing, count, game_map, start_row, start_col):
    new_row = start_row
    new_col = start_col

    # What is the row, col increment for each facing?
    in_lookup = {'L': (-1, 0), 'R': (1, 0), 'D': (0, 1), 'U': (0, -1)}

    if facing in ['L', 'R']:
        for idx in range(count):
            temp = new_col
            new_col = (new_col + in_lookup[facing][0]) % game_map.shape[1]
            if game_map[start_row][new_col] == WALL:
                new_col = temp
                break
            elif game_map[start_row][new_col] == NULL:
                rc = wrap_around_move(game_map, start_row, temp, facing)
                if not rc:
                    new_col = temp
                    break
                else:
                    new_col = rc[1]
                    continue
    else:  # Up/down
        for idx in range(count):
            temp = new_row
            new_row = (new_row + in_lookup[facing][1]) % game_map.shape[0]
            if game_map[new_row][start_col] == WALL:
                new_row = temp
                break
            elif game_map[new_row][start_col] == NULL:
                rc = wrap_around_move(game_map, temp, start_col, facing)
                if not rc:
                    new_row = temp
                    break
                new_row = rc[0]
                continue

    if idx + 1 != count:
        print(f"{idx + 1} {facing} out of {count} moves")
    else:
        print(f'Moved {count} {facing}')
    return new_row, new_col


if __name__ == '__main__':
    if False:  # Brad trick for sample/file toggle
        tokens = sample.split('\n\n')
    else:
        tokens = open(DATAFILE).read().split('\n\n')
    game_map = parse_map(clean_data_lines(tokens[0].split('\n')))
    directions = parse_directions(tokens[1].strip())
    row, col, facing = find_start(game_map)
    for step in directions:
        print(f"Starting {row=} {col=} {facing=} {step=}")
        row, col = move(facing, step[0], game_map, row, col)
        if step[1]:
            facing = new_direction(facing, step[1])

    print(f"{calc_password(row, col, facing)=} {row=} {col=} {facing=} {len(directions)=}")
