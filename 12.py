
DATAFILE = './data/12.txt'

test_data = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

test_solution = """
v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^
"""

test_move_count = 31


def to_int(input):
    return ord(input) - ord('a')


def test_to_int():
    assert to_int('a') == 0
    assert to_int('z') == 25


def parse_input(data_lines):
    # Return a tuple - start (row, col)
    # end (row, col)
    # 2D elevation map [[]]

    row_count = col_count = 0
    start = tuple()
    end = tuple()
    elevation_map = []

    row_idx = 0
    for line in data_lines:
        if len(line) == 0:
            continue

        elevation_map.append([])
        col_idx = 0
        for cell in line:
            match cell:
                case 'S':
                    start = (row_idx, col_idx, )
                    elevation_map[row_idx].append(0)
                case 'E':
                    end = (row_idx, col_idx, )
                    elevation_map[row_idx].append(to_int('z'))
                case _:
                    elevation_map[row_idx].append(to_int(cell))
            col_idx += 1
        row_idx += 1
    print(f"{start} {end}")
    print(elevation_map)

    return(start, end, elevation_map)


def to_adjacency(map):
    # For each cell/vertex, the LRUD cells are ajdacent if the height difference is <= 1.
    pass



if __name__ == '__main__':
    test_to_int()
    parse_input(test_data.split('\n'))
