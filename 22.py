import numpy as np
from numpy import NaN

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
sample_moves='10R5L5R10L4R5L5'


def parse_data(data_lines):
    num_rows = len(data_lines)
    num_cols = max([len(x) for x in data_lines])
    rc = np.zeros((num_rows, num_cols), dtype=np.int16)

    for row_idx, row in enumerate(data_lines):
        if len(row) == 0:
            continue
        for col_idx, char in enumerate(row):
            temp = None
            if char == ' ':
                temp = 0
            elif char == '.':
                temp = 1
            elif char == '#':
                temp = 2
            np.put(rc, [row_idx, col_idx], [temp])
            # rc[row_idx][col_idx] = temp
    return rc

if __name__ == '__main__':
    q = parse_data(sample_map.split(('\n')))
    pass
