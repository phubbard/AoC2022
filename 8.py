
from typing import List

test_data = [
    '30373',
    '25512',
    '65332',
    '33549',
    '35390',
]

test_viz_count = 21
DATAFILE = './data/8.txt'


def parse_lines(data_lines) -> List[List[int]]:
    rc = []
    for line in data_lines:
        row_array = []
        cur_line = line.strip()
        for col in range(len(cur_line)):
            row_array.append(int(cur_line[col]))
        rc.append(row_array)
    return rc


def recalc_visibility(data):
    rows = len(data[0])
    cols = rows # Hardwired for square
    # Weird corner rules but shrug
    viz_count = ((2 * rows) + (2 * cols)) - 4
    print(f'Edge count {viz_count}')

    for row_idx in range(1, rows - 1):
        for col_idx in range(1, cols - 1):
            cur_height = data[row_idx][col_idx]
            left_viz = 1
            right_viz = 1
            if max(data[row_idx][0: col_idx]) >= cur_height:
                left_viz = 0
            if max(data[row_idx][col_idx + 1:]) >= cur_height:
                right_viz = 0

            # No way to extract a column without numpy so Just Deal.
            col = [row[col_idx] for row in data]
            up_viz = 1
            down_viz = 1
            if max(col[0: row_idx]) >= cur_height:
                up_viz = 0
            if max(col[row_idx + 1:]) >= cur_height:
                down_viz = 0

            if up_viz + down_viz + left_viz + right_viz > 0:
                viz_count += 1

    return viz_count


def run_test_data():
    data = parse_lines(test_data)
    count = recalc_visibility(data)
    print(f"{count} found, should be 21")
    assert count == test_viz_count


def run_step():
    data_lines = open(DATAFILE, 'r')
    data = parse_lines(data_lines)
    count = recalc_visibility(data)
    print(f"{count} found in data file")


if __name__ == '__main__':
    run_test_data()
    run_step()

