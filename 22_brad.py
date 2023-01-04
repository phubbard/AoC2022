
import collections

sample_data = """        ...#
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

10R5L5R10L4R5L5
"""
sample_answer_a = 6032
DATAFILE = './data/22.txt'

DIRECTION_NORTH = '*North*'
DIRECTION_SOUTH = '*South*'
DIRECTION_EAST  = '*East*'
DIRECTION_WEST  = '*West*'

DIRECTIONS_ALL = (DIRECTION_NORTH,
                  DIRECTION_SOUTH,
                  DIRECTION_EAST,
                  DIRECTION_WEST)

SQUARE_NONE = ' '
SQUARE_WALL = '#'
SQUARE_OPEN = '.'


def log(some_string):
    print(f"P22: {some_string}")


class Square:
    def __init__(self, row, column, is_open, is_wall):
        self.SQUARE_ROW     = row
        self.SQUARE_COLUMN  = column
        self.SQUARE_IS_OPEN = is_open
        self.SQUARE_IS_WALL = is_wall

        self.__directions = {}

    def square_connect(self, direction, square):
        self.__directions[direction] = square

    def square_neighbor(self, direction):
        return self.__directions[direction]

    def __str__(self):
        wall_string = " WALL" if self.SQUARE_IS_WALL else ""
        return f"({self.SQUARE_ROW}, {self.SQUARE_COLUMN}){wall_string}"



class Grove:
    def __init__(self, max_row, max_col):
        self.GROVE_MIN_ROW =   0
        self.GROVE_MAX_ROW = max_row

        self.GROVE_MIN_COL =   0
        self.GROVE_MAX_COL = max_col

        self.__build_row = 1
        self.__squares   = collections.OrderedDict()

    def grove_build_add_stripe(self, stripe):
        """Consume the first sequence of rows of input, returning True if and
        only if it is the blank line that separates the grove geometry from
        the direction string.
        """

        if len(stripe.strip()) == 0:
            return True

        current_stripe = collections.OrderedDict()

        log(f"Row:{self.__build_row}... -> {stripe}")
        for idx, char in enumerate(stripe):
            if stripe[idx] == SQUARE_NONE: continue
            column = idx + 1
            square = Square(self.__build_row, column, char == SQUARE_OPEN, char == SQUARE_WALL)
            current_stripe[column] = square
            log(f"  at {self.__build_row} {column} saw {char}")
        log(f"   and ends at at {column}.")

        self.__squares[self.__build_row] = current_stripe
        self.__build_row += 1
        return False

    def grove_locate_square(self, row, col):
        stripe = self.__squares.get(row, None)
        if stripe is None: return None
        return stripe.get(col, None)

    def __grove_forge(self, direction, first, prev, row, col):
        """Cause any previous square to point to the current one, and
        assure that current square, if present, points to first one.
        This gets rewritten each time.  This is a utility reusable for
        each direction.
        """

        current = self.grove_locate_square(row, col)

        if prev and current: prev.square_connect(direction, current)
        if current:          current.square_connect(direction, first)

        new_first = first or current
        new_prev  = current
        return new_first, new_prev

    def grove_seal(self):
        f"""This function performs 4 passes once all {Square}s are populated;
        one in each of the cardinal directions.  Each {Square} gets linked to
        the {Square}s in the appropriate direction, including wrap conditions.
        """

        # WEST
        for row in range(self.GROVE_MIN_ROW, self.GROVE_MAX_ROW, 1):
            first, prev = (None, None, )
            for col in range(self.GROVE_MIN_COL, self.GROVE_MAX_COL, 1):
                first, prev = self.__grove_forge(DIRECTION_EAST, first, prev, row, col)

        # EAST
        for row in range(self.GROVE_MIN_ROW, self.GROVE_MAX_ROW, 1):
            first, prev = (None, None, )
            for col in range(self.GROVE_MAX_COL, self.GROVE_MIN_COL, -1):
                first, prev = self.__grove_forge(DIRECTION_WEST, first, prev, row, col)

        # SOUTH
        for col in range(self.GROVE_MIN_COL, self.GROVE_MAX_COL, 1):
            first, prev = (None, None, )
            for row in range(self.GROVE_MIN_ROW, self.GROVE_MAX_ROW, 1):
                first, prev = self.__grove_forge(DIRECTION_SOUTH, first, prev, row, col)

        # NORTH
        for col in range(self.GROVE_MIN_COL, self.GROVE_MAX_COL, 1):
            first, prev = (None, None, )
            for row in range(self.GROVE_MAX_ROW, self.GROVE_MIN_ROW, -1):
                first, prev = self.__grove_forge(DIRECTION_NORTH, first, prev, row, col)

        pass


class Directions:
    def __init__(self, raw_string):
        self.DIRECTIONS_RAW_STRING = raw_string


def parse_data(data_string, grove):
    do_directions = False
    directions = None
    stripes = data_string.split("\n")
    for stripe in stripes:
        if do_directions:
            directions = Directions(stripe)
        else:
            do_directions = grove.grove_build_add_stripe(stripe)
    return directions
    

if __name__ == '__main__':

    if True:
        pure_input        = sample_data
        expected_answer_a = sample_answer_a
        grove             = Grove(20, 20)
    else:
        pure_input        = open(DATAFILE, 'r').read()
        expected_answer_a = -1
        grove             = Grove(210, 210)

    directions = parse_data(pure_input, grove)

    grove.grove_seal()

    log(f"Starting test...")
    square = grove.grove_locate_square(6, 8) # Wall South, Wall East
    log(f"anchor: {str(square)}")
    for direction in DIRECTIONS_ALL:
        neighbor = square.square_neighbor(direction)
        log(f"   {direction}: {str(neighbor)}")

    walk = 20
    direction = DIRECTION_SOUTH
    log(f"Lets go {direction} {walk=} steps...")
    for _ in range(walk):
        square = square.square_neighbor(direction)
        log(f"next: {str(square)}")

    log(f"No fails.")


