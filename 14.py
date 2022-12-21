DATAFILE = "./data/14.txt"

sample_data = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

sample_answer = 34


def down(current):
    return current[0] - 1, current[1]


def down_left(current):
    return current[0] - 1, current[1] - 1


def down_right(current):
    return current[0] - 1, current[1] + 1


def drop_sand(map, min_x_val):
    # Returns ending coordinates
    map[500, 0] = 'o'
    current_coordinates = (500, 0,)

    while current_coordinates[0] >= min_x_val:
        if map[down(current_coordinates)] == '.':
            current_coordinates = down(current_coordinates)
        elif map[down_left(current_coordinates)] == '.':
            current_coordinates = down_left(current_coordinates)
        elif map[down_right(current_coordinates)] == '.':
            current_coordinates = down_right(current_coordinates)
        else:
            # FIXME flag ending condition. How do we discern end vs keep-here?
            break
    return current_coordinates
