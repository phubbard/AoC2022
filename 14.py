import logging
import sys


DATAFILE = "./data/14.txt"

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(message)s')
log = logging.getLogger()



SAMPLE_DATA = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

SAMPLE_ANSWER = 34


class Point:
    def __init__(self, x, y):
        self.POINT_X = x
        self.POINT_Y = y

    def __str__(self): return f"({self.POINT_X}, {self.POINT_Y})"


class Scan:
    def __init__(self, list_of_points):
        self.SCAN_SEGMENTS = tuple(list_of_points)


class Slice:

    ICON_EMPTY  = '.'
    ICON_ROCK   = '#'
    ICON_SAND   = 'o'
    ICON_SOURCE = '+'
    ICON_VOID   = '~'

    def __init__(self, scan):

        MAX_INT = +99999999
        MIN_INT = -99999999

        min_x = MAX_INT
        min_y = MAX_INT
        max_x = MIN_INT
        max_y = MIN_INT

        for segment in scan.SCAN_SEGMENTS:
            for point in segment:
                min_x = min(min_x, point.POINT_X)
                min_y = min(min_y, point.POINT_Y)
                max_x = max(max_x, point.POINT_X)
                max_y = max(max_y, point.POINT_Y)

        self.SLICE_SOURCE_X = 500
        self.SLICE_SOURCE_Y =   0

        self.SLICE_SCAN     = scan
        self.SLICE_MIN_X    = min_x - 1
        self.SLICE_MIN_Y    = min(min_y, self.SLICE_SOURCE_Y) - 1
        self.SLICE_MAX_X    = max_x + 1
        self.SLICE_MAX_Y    = max_y + 1
        self.SLICE_WIDTH    = self.SLICE_MAX_X - self.SLICE_MIN_X + 1
        self.SLICE_HEIGHT   = self.SLICE_MAX_Y - self.SLICE_MIN_Y + 1

        self.SLICE_SOURCE   =   (self.SLICE_SOURCE_X, self.SLICE_SOURCE_Y, )

        log.info(f"SLICE_MIN_X  :{self.SLICE_MIN_X}")
        log.info(f"SLICE_MIN_Y  :{self.SLICE_MIN_Y}")
        log.info(f"SLICE_MAX_X  :{self.SLICE_MAX_X}")
        log.info(f"SLICE_MAX_Y  :{self.SLICE_MAX_Y}")
        log.info(f"SLICE_WIDTH  :{self.SLICE_WIDTH}")
        log.info(f"SLICE_HEIGHT :{self.SLICE_HEIGHT}")

        grid = []
        for y in range(self.SLICE_HEIGHT):
            row = []
            for x in range(self.SLICE_WIDTH):
                row.append(Slice.ICON_EMPTY)
            grid.append(row)
        self.__slice_grid = grid

        def better_range(start_value, finish_value):
            step_size = 1 if start_value < finish_value else -1
            return list(range(start_value, finish_value + step_size, step_size))

        # initial linedraw
        for segment in scan.SCAN_SEGMENTS:
            last_point = None
            for point in segment:
                if last_point is not None:
                    log.info(f"Attempting draw from {last_point} to {point}...")
                    is_horizontal = last_point.POINT_X == point.POINT_X
                    if is_horizontal:
                        for y in better_range(last_point.POINT_Y, point.POINT_Y):
                            self.place_rock_at((last_point.POINT_X, y))
                    else:
                        for x in better_range(last_point.POINT_X, point.POINT_X):
                            self.place_rock_at((x, last_point.POINT_Y))
                last_point = point
        return

    def absolute_to_relative(self, absolute_coordinate):
        return (absolute_coordinate[0] - self.SLICE_MIN_X,
                absolute_coordinate[1] - self.SLICE_MIN_Y, )

    def slice_render(self):
        for row in self.__slice_grid:
            string_row = "".join(row)
            log.info(string_row)

    def get_icon_at(self, position_tuple):
        delta_x, delta_y = self.absolute_to_relative(position_tuple)
        rv = self.__slice_grid[delta_y][delta_x]
        log.info(f"Found a {rv} at   PURE {position_tuple[0]} {position_tuple[1]}    RELATIVE {delta_x} {delta_y}")

        return rv

    def place_at(self, icon, position_tuple):
        delta_x, delta_y = self.absolute_to_relative(position_tuple)
        log.info(f"Placing {icon} at  PURE {position_tuple[0]} {position_tuple[1]}    RELATIVE {delta_x} {delta_y}")

        self.__slice_grid[delta_y][delta_x] = icon

    def place_sand_at(self, position_tuple): 
        self.place_at(self.ICON_SAND, position_tuple)

    def place_rock_at(self, position_tuple): 
        self.place_at(self.ICON_ROCK, position_tuple)



def down(current):
    return current[0], current[1] + 1


def down_left(current):
    return current[0] - 1, current[1] + 1


def down_right(current):
    return current[0] + 1, current[1] + 1


def drop_sand(slice):

    # Returns ending coordinates
    current_coordinates = slice.SLICE_SOURCE

    fell_off_bottom = False
    while True:
        log.info(f"dropping next is -> {current_coordinates}")
        fell_off_bottom = current_coordinates[1] >= slice.SLICE_MAX_Y
        if slice.get_icon_at(down(current_coordinates)) == slice.ICON_EMPTY:
            current_coordinates = down(current_coordinates)
        elif slice.get_icon_at(down_left(current_coordinates)) == slice.ICON_EMPTY:
            current_coordinates = down_left(current_coordinates)
        elif slice.get_icon_at(down_right(current_coordinates)) == slice.ICON_EMPTY:
            current_coordinates = down_right(current_coordinates)
        else:
            # FIXME flag ending condition. How do we discern end vs keep-here?
            break
    return None if fell_off_bottom else current_coordinates


def parse_input(text):
    scans = text.strip().split("\n")
    stored_segments = []
    for scan in scans:
        current_segment = []
        log.info(f"SCAN...")
        raw_points = scan.split(" -> ")
        for raw_point in raw_points:
            x, y = eval(f"({raw_point})")
            log.info(f"    POINT {x} {y}")
            current_segment.append(Point(x, y))
        log.info(f"   END")
        stored_segments.append(current_segment)
    rv = Scan(stored_segments)
    return rv


if __name__ == '__main__':
    if True:
        scan = parse_input(SAMPLE_DATA)
    else:
        scan = parse_input(open(DATAFILE, 'r').read())

    slice = Slice(scan)

    slice.slice_render()
    for x in range(5):
        end_coordinates = drop_sand(slice)
        if end_coordinates is not None:
            slice.place_sand_at(end_coordinates)
        slice.slice_render()

    


