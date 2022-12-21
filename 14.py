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

    def __str__(self): return f"({self.POINT_X}, {self.POINT_X})"


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

        self.SLICE_SCAN     = scan
        self.SLICE_MIN_X    = min_x - 1
        self.SLICE_MIN_Y    = min_y - 1
        self.SLICE_WIDTH    = max_x - min_x + 2
        self.SLICE_HEIGHT   = max_y - min_y + 2

        self.SLICE_SOURCE_X = 500
        self.SLICE_SOURCE_Y =   0

        grid = []
        for y in range(self.SLICE_HEIGHT):
            row = []
            for x in range(self.SLICE_WIDTH):
                row.append(Slice.ICON_EMPTY)
            grid.append(row)

        # initial linedraw
        for segment in scan.SCAN_SEGMENTS:
            last_point = None
            for point in segment:
                if last_point is not None: 
                    # Draw line
                    pass
                last_point = point

        self.__slice_grid = grid


    def slice_render(self):
        for row in self.__slice_grid:
            string_row = "".join(row)
            log.info(string_row)

    def get_icon_at(self, x, y):
        pass

    def place_sand_at(self, x, y):
        pass


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

    log.info(f"SLICE_MIN_X  :{slice.SLICE_MIN_X}")
    log.info(f"SLICE_MIN_Y  :{slice.SLICE_MIN_Y}")
    log.info(f"SLICE_WIDTH  :{slice.SLICE_WIDTH}")
    log.info(f"SLICE_HEIGHT :{slice.SLICE_HEIGHT}")

    slice.slice_render()
    


