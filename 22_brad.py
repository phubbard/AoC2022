
import collections

sample_data = """
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

10R5L5R10L4R5L5
"""
sample_answer_a = 6032
DATAFILE = './data/22.txt'

DIRECTION_NORTH = 'n'
DIRECTION_SOUTH = 's'
DIRECTION_EAST  = 'e'
DIRECTION_WEST  = 'w'


class Square:
    def __init__(self, is_open, is_wall):
        self.SQUARE_IS_OPEN = is_open
        self.SQUARE_IS_WALL = is_wall

        self.__directions = {}

    def square_connect(self, direction, square):
        self.__directions[direction] = square


SQUARE_NONE = ' '
SQUARE_WALL = '#'
SQUARE_OPEN = '.'


class Grove:
    def __init__(self):
        self.GROVE_MIN_ROW =   0
        self.GROVE_MAX_ROW = 210

        self.GROVE_MIN_COL =   0
        self.GROVE_MAX_COL = 160

        self.__build_row = 0
        self.__squares   = collections.OrderedDict()

    def grove_build_add_stripe(self, stripe):
        """Consume the first sequence of rows of input, returning True if and
        only if it is the blank line that separates the grove geometry from
        the direction string.
        """

        if len(stripe.strip() == 0):
            return True

        current_stripe = collections.OrderedDict()
        start_column = 0
        while stripe[start_column] == SQUARE_NONE:
            start_column += 1
        for column, char in enumerate(stripe, start=start_column):
            square = Square(char == SQUARE_OPEN, char == SQUARE_WALL)
            current_stripe[column] = square

        self.__squares[self.__build_row] = current_stripe
        self.__build_row += 1
        return False

    def grove_locate_square(self, row, col):
        stripe = self_squares.get(row, None)
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
        first, prev = (None, None, )
        for row in range(self.GROVE_MIN_ROW, self.GROVE_MAX_ROW, 1):
            for col in range(self.GROVE_MIN_COL, self.GROVE_MAX_COL, 1):
                first, prev = self.__grove_forge(DIRECTION_WEST, first, prev, row, col)

        # EAST
        first, prev = (None, None, )
        for row in range(self.GROVE_MIN_ROW, self.GROVE_MAX_ROW, 1):
            for col in range(self.GROVE_MAX_COL, self.GROVE_MIN_COL, -1):
                first, prev = self.__grove_forge(DIRECTION_EAST, first, prev, row, col)

        # SOUTH
        first, prev = (None, None, )
        for col in range(self.GROVE_MIN_COL, self.GROVE_MAX_COL, 1):
            for row in range(self.GROVE_MIN_ROW, self.GROVE_MAX_ROW, 1):
                first, prev = self.__grove_forge(DIRECTION_SOUTH, first, prev, row, col)

        # NORTH
        first, prev = (None, None, )
        for col in range(self.GROVE_MIN_COL, self.GROVE_MAX_COL, 1):
            for row in range(self.GROVE_MAX_ROW, self.GROVE_MIN_ROW, -1):
                first, prev = self.__grove_forge(DIRECTION_NORTH, first, prev, row, col)

        pass


class Directions:
    def __init__(self, direction_string):
        pass


def parse_data(data_string):
    for line in data_string.strip().split("\n"):
        pass

if __name__ == '__main__':

    if False:
        pure_input        = sample_data
        expected_answer_a = sample_answer_a
    else:
        pure_input        = open(DATAFILE, 'r').read()
        expected_answer_a = -1

    grove, directions = parse_data(pure_input)


