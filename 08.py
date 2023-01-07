
from typing import List

test_data = [
    '30373',
    '25512',
    '65332',
    '33549',
    '35390',
]

test_viz_count = 21
test_scenic_max = 8
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


def calc_visibility(data) -> int:
    rows = len(data[0])
    cols = rows
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


def calc_scenic_vec(vector) -> int:
    if len(vector) == 0:
        return 0

    tzero = vector[0]
    count = 0
    idx = 1
    while idx < len(vector):
        count += 1
        if vector[idx] >= tzero:
            break
        idx += 1

    return count


def calc_scenic_max(data) -> int:
    rows = len(data[0])
    cols = rows

    max_score = 0
    for row_idx in range(0, rows):
        for col_idx in range(0, cols):
            left_look = data[row_idx][0:col_idx + 1]
            left_look.reverse()
            left_count = calc_scenic_vec(left_look)

            right_look = data[row_idx][col_idx:]
            right_count = calc_scenic_vec(right_look)

            col = [row[col_idx] for row in data]
            up_look = col[0: row_idx + 1]
            up_look.reverse()
            up_count = calc_scenic_vec(up_look)

            down_look = col[row_idx:]
            down_count = calc_scenic_vec(down_look)

            cur_score = left_count * right_count * up_count * down_count
            if cur_score > max_score:
                max_score = cur_score

    print(f'Max score {max_score}')
    return max_score


def run_test_data():
    data = parse_lines(test_data)
    count = calc_visibility(data)
    print(f"{count} found, should be {test_viz_count}")
    assert count == test_viz_count
    view_max = calc_scenic_max(data)
    print(f"{view_max} scenic max found, should be {test_scenic_max}")
    assert view_max == test_scenic_max


def run_step():
    data = parse_lines(open(DATAFILE, 'r'))
    count = calc_visibility(data)
    scenic_best = calc_scenic_max(data)
    print(f"{count} found in data file, scene max {scenic_best}")


if __name__ == '__main__':
    run_test_data()
    run_step()
