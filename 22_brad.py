
import collections


sample_answer_a = 6032
sample_answer_b = 5031

SAMPLE_DATAFILE = './data/22_sample.txt'
DATAFILE = './data/22.txt'

DIRECTION_NORTH = '*North*'
DIRECTION_SOUTH = '*South*'
DIRECTION_EAST  = '*East*'
DIRECTION_WEST  = '*West*'

DIRECTIONS_ALL = (DIRECTION_NORTH,
                  DIRECTION_SOUTH,
                  DIRECTION_EAST,
                  DIRECTION_WEST)

DIRECTIONS_RIGHT = {
        DIRECTION_NORTH: DIRECTION_EAST,
        DIRECTION_EAST:  DIRECTION_SOUTH,
        DIRECTION_SOUTH: DIRECTION_WEST,
        DIRECTION_WEST:  DIRECTION_NORTH,
    }

DIRECTIONS_LEFT = {
        DIRECTION_NORTH: DIRECTION_WEST,
        DIRECTION_EAST:  DIRECTION_NORTH,
        DIRECTION_SOUTH: DIRECTION_EAST,
        DIRECTION_WEST:  DIRECTION_SOUTH,
    }

DIRECTIONS_REVERSE = {
        DIRECTION_NORTH: DIRECTION_SOUTH,
        DIRECTION_EAST:  DIRECTION_WEST,
        DIRECTION_SOUTH: DIRECTION_NORTH,
        DIRECTION_WEST:  DIRECTION_EAST,
    }

DIRECTIONS_FACING = {
        DIRECTION_NORTH: 3,
        DIRECTION_EAST:  0,
        DIRECTION_SOUTH: 1,
        DIRECTION_WEST:  2,
    }

DIRECTIONS_PAUL = {
        DIRECTION_NORTH: 'U',
        DIRECTION_EAST:  'R',
        DIRECTION_SOUTH: 'D',
        DIRECTION_WEST:  'L',
    }

SQUARE_NONE = ' '
SQUARE_WALL = '#'
SQUARE_OPEN = '.'


def log(some_string):
    print(f"P22: {some_string}")

def paullog(some_string):
    print(f"{some_string}")


class Warp:
    def __init__(self, square, direction):
        self.WARP_SQUARE    = square
        self.WARP_DIRECTION = direction


class Square:
    def __init__(self, row, column, is_open, is_wall):
        self.SQUARE_ROW     = row
        self.SQUARE_COLUMN  = column
        self.SQUARE_IS_OPEN = is_open
        self.SQUARE_IS_WALL = is_wall

        self.__directions = {}
        self.__warps      = {}


    def square_connect(self, direction, square):
        self.__directions[direction] = square

    def square_tunnel(self, leave_direction, square, new_direction):
        self.__warps[leave_direction] = Warp(square, new_direction)

    def square_neighbor(self, direction):
        return (direction, self.__directions[direction], )

    def square_warp(self, direction):
        warp = self.__warps.get(direction, None)
        if warp is None:
            # if no warp in specified direction, we just do the 2 space thing
            return self.square_neighbor(direction)
        else:
            # Otherwise take the warp which will change the direction as well
            return (warp.WARP_DIRECTION, warp.WARP_SQUARE, )

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

        #log(f"Row:{self.__build_row}... -> {stripe}")
        for idx, char in enumerate(stripe):
            if stripe[idx] == SQUARE_NONE: continue
            column = idx + 1
            square = Square(self.__build_row, column, char == SQUARE_OPEN, char == SQUARE_WALL)
            current_stripe[column] = square
            #log(f"  at {self.__build_row} {column} saw {char}")
        #log(f"   and ends at at {column}.")

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


TURN_LEFT  = 'L'
TURN_RIGHT = 'R'


class Step:
    def __init__(self, number_steps=None, turn=None):
        self.STEP_NUMBER_STEPS  = number_steps
        self.STEP_TURN          = turn

        log(f"CREATED STEP -> {str(self)}")

    def __str__(self):
        if self.STEP_TURN: return f"TURN {self.STEP_TURN}"
        else:              return f"STEP {self.STEP_NUMBER_STEPS}"


class Instructions:
    def __init__(self, raw_string, starting_direction):

        direction = starting_direction
        sequence = []

        split_right = raw_string.split("R")
        for right_index, right_segment in enumerate(split_right):
            if right_index > 0:
                direction = DIRECTIONS_RIGHT[direction]
                sequence.append(Step(turn=TURN_RIGHT))
            split_left = right_segment.split("L")
            for step_index, step_string in enumerate(split_left):
                if step_index > 0:
                    direction = DIRECTIONS_LEFT[direction]
                    sequence.append(Step(turn=TURN_LEFT))
                if len(step_string) > 0:
                    sequence.append(Step(number_steps=int(step_string)))

        self.INSTRUCTIONS_RAW      = raw_string
        self.INSTRUCTIONS_SEQUENCE = tuple(sequence)

    def __str__(self):
        inner = [str(step) for step in self.INSTRUCTIONS_SEQUENCE]
        as_string = ','.join(inner)
        return f"<INSTRUCTIONS {as_string} >"


class Coordinate:
    def __init__(self, a_tuple):
        self.COORDINATE_ROW   = a_tuple[0]
        self.COORDINATE_COL   = a_tuple[1]
        self.COORDINATE_TUPLE = (self.COORDINATE_ROW,
                                 self.COORDINATE_COL)

    def __add__(self, other):
        return Coordinate((self.COORDINATE_ROW + other.COORDINATE_ROW,
                           self.COORDINATE_COL + other.COORDINATE_COL))

    def __sub__(self, other):
        return Coordinate((self.COORDINATE_ROW - other.COORDINATE_ROW,
                           self.COORDINATE_COL - other.COORDINATE_COL))

    def __str__(self):
        return f"({self.COORDINATE_ROW}, {self.COORDINATE_COL})"

    def __eq__(self, other):
        row = self.COORDINATE_ROW - other.COORDINATE_ROW
        col = self.COORDINATE_COL - other.COORDINATE_COL
        log(f" While checking {self} equals {other}, saw {row=} and {col=}")
        return row == 0 and col == 0

    def planck_step(self, other):
        row = other.COORDINATE_ROW - self.COORDINATE_ROW
        col = other.COORDINATE_COL - self.COORDINATE_COL
        if row > 0: row = +1
        if row < 0: row = -1
        if col > 0: col = +1
        if col < 0: col = -1
        rv = Coordinate((row, col))

        log(f"Planck step from {self} to {other} has {row=} and {col=} and therefore {rv}")

        return rv


def generate_warps(grove,
                   alpha_leave_direction,
                   alpha_start_tuple,
                   alpha_terminal_tuple,
                   alpha_new_direction,
                   beta_leave_direction,
                   beta_start_tuple,
                   beta_terminal_tuple,
                   beta_new_direction):

    alpha_start    = Coordinate(alpha_start_tuple)
    alpha_terminal = Coordinate(alpha_terminal_tuple)

    beta_start    = Coordinate(beta_start_tuple)
    beta_terminal = Coordinate(beta_terminal_tuple)

    alpha_stepper = alpha_start.planck_step(alpha_terminal)
    beta_stepper  = beta_start.planck_step(beta_terminal)

    alpha_working = alpha_start
    beta_working  = beta_start

    is_finished = False
    while not is_finished:
        log(f"adding warp from {alpha_working} to {beta_working}")
        alpha_square = grove.grove_locate_square(*alpha_working.COORDINATE_TUPLE)
        beta_square  = grove.grove_locate_square(*beta_working.COORDINATE_TUPLE)

        alpha_square.square_tunnel(alpha_leave_direction, beta_square,  alpha_new_direction)
        beta_square.square_tunnel(beta_leave_direction,   alpha_square, beta_new_direction)

        alpha_finished = (alpha_working == alpha_terminal)
        beta_finished  = (beta_working  == beta_terminal)

        if alpha_finished != beta_finished: raise Exception("Woe is me")

        alpha_working = alpha_working + alpha_stepper
        beta_working  = beta_working  + beta_stepper

        is_finished = alpha_finished and beta_finished

        log(f"{alpha_finished=} and {beta_finished=} causing {is_finished=}")


    return


def parse_data(data_string, grove):
    do_instructions = False
    instructions    = None
    stripes = data_string.split("\n")
    for stripe in stripes:
        if do_instructions:
            instructions = Instructions(stripe, DIRECTION_EAST)
            break
        else:
            do_instructions = grove.grove_build_add_stripe(stripe)
    return instructions
    

if __name__ == '__main__':

    do_sample = False

    if do_sample:
        pure_input        = open(SAMPLE_DATAFILE, 'r').read()
        expected_answer_a = sample_answer_a
        expected_answer_b = sample_answer_b
        grove             = Grove(20, 20)
    else:
        pure_input        = open(DATAFILE, 'r').read()
        expected_answer_a = 36518
        expected_answer_b = 143208  # 55339 is TOO LOW
        grove             = Grove(210, 210)

    instructions = parse_data(pure_input, grove)

    grove.grove_seal()

    if do_sample:
        # Warps for sample data
        generate_warps(grove,
                       DIRECTION_NORTH,  (5,  5),  (5,  8), DIRECTION_EAST,
                       DIRECTION_WEST,   (1,  9),  (4,  9), DIRECTION_SOUTH)
        generate_warps(grove,
                       DIRECTION_NORTH,  (5,  1),  (5,  4), DIRECTION_SOUTH,
                       DIRECTION_NORTH,  (1, 12),  (1,  9), DIRECTION_SOUTH)
        generate_warps(grove,
                       DIRECTION_WEST,   (5,  1),  (8,  1), DIRECTION_NORTH,
                       DIRECTION_SOUTH, (12, 16), (12, 13), DIRECTION_EAST)
        generate_warps(grove,
                       DIRECTION_SOUTH,  (8,  1),  (8,  4), DIRECTION_NORTH,
                       DIRECTION_SOUTH, (12, 12), (12,  9), DIRECTION_NORTH)
        generate_warps(grove,
                       DIRECTION_WEST,   (5,  1),  (8, 1),  DIRECTION_NORTH,
                       DIRECTION_SOUTH, (12, 16), (12, 13), DIRECTION_EAST)
        generate_warps(grove,
                       DIRECTION_EAST,   (9, 16), (12, 16), DIRECTION_WEST,
                       DIRECTION_WEST,   (4, 12),  (1, 12), DIRECTION_EAST)
        generate_warps(grove,
                       DIRECTION_NORTH,  (9, 13),  (9, 16), DIRECTION_WEST,
                       DIRECTION_EAST,   (8, 12),  (5, 12), DIRECTION_SOUTH)

    else:
        # Warps for real data
        generate_warps(grove,
                       DIRECTION_NORTH, (1,   51),  (1,   100), DIRECTION_EAST,
                       DIRECTION_WEST,  (151, 1),   (200, 1),   DIRECTION_SOUTH)
        generate_warps(grove,
                       DIRECTION_SOUTH, (200, 1),   (200, 50),  DIRECTION_SOUTH,
                       DIRECTION_NORTH, (1,   101), (1,   150), DIRECTION_NORTH)
        generate_warps(grove,
                       DIRECTION_EAST,  (51, 100),  (100, 100), DIRECTION_NORTH,
                       DIRECTION_SOUTH, (50, 101),  (50,  150), DIRECTION_WEST)
        generate_warps(grove,
                       DIRECTION_WEST,  (51,  51),  (100, 51),  DIRECTION_SOUTH,
                       DIRECTION_NORTH, (101, 1),   (101, 50),  DIRECTION_EAST)
        generate_warps(grove,
                       DIRECTION_WEST,  (101, 1),   (150, 1),   DIRECTION_EAST,
                       DIRECTION_WEST,  (50,  51),  (1,   51),  DIRECTION_EAST)
        generate_warps(grove,
                       DIRECTION_EAST,  (151, 50),  (200, 50),  DIRECTION_NORTH,
                       DIRECTION_SOUTH, (150, 51),  (150, 100), DIRECTION_WEST)
        generate_warps(grove,
                       DIRECTION_EAST,  (1,   150), (50,  150), DIRECTION_WEST,
                       DIRECTION_EAST,  (150, 100), (101, 100), DIRECTION_WEST)

    def _do_test_sequence():
        log(f"Starting test...")
        square = grove.grove_locate_square(6, 8) # Wall South, Wall East
        log(f"anchor: {str(square)}")
        for direction in DIRECTIONS_ALL:
            neighbor = square.square_neighbor(direction)
            log(f"   {direction}: {str(neighbor)}")

        walk = 20
        direction = DIRECTION_EAST
        log(f"Lets go {direction} {walk=} steps...")
        for _ in range(walk):
            square = square.square_neighbor(direction)
            log(f"next: {str(square)}")
    # _do_test_sequence()

    log(f"Instructions -> {str(instructions)}")

    log(f"Locate start square...")
    start_row, start_col = 1, 1
    square = None
    while True:
        current_square = grove.grove_locate_square(start_row, start_col)
        if current_square is not None:
            break
        start_col += 1
    log(f"Start square found -> {str(current_square)}")

    log(f"Starting instruction interpretation part A style...")
    current_direction = DIRECTION_EAST

    for step in instructions.INSTRUCTIONS_SEQUENCE:

        if step.STEP_TURN == TURN_RIGHT:
            current_direction = DIRECTIONS_RIGHT[current_direction]
        elif step.STEP_TURN == TURN_LEFT:
            current_direction = DIRECTIONS_LEFT[current_direction]
        else:
            step_count = step.STEP_NUMBER_STEPS

            paullog(f"Begin {current_square.SQUARE_ROW - 1}, {current_square.SQUARE_COLUMN - 1} {DIRECTIONS_PAUL[current_direction]} {step_count}")

            #log(f"Starting {step_count} steps in {current_direction=}")
            for _ in range(step_count):
                next_direction, next_square = current_square.square_warp(current_direction)
                if next_square.SQUARE_IS_WALL:
                    # log(f"Stuck since next is {str(next_square)}")
                    continue
                else:
                    # log(f"Moving to {str(next_square)}")
                    current_square = next_square
                    current_direction = next_direction

            paullog(f"End {current_square.SQUARE_ROW - 1}, {current_square.SQUARE_COLUMN - 1}")

    final_facing = DIRECTIONS_FACING[current_direction]
    final_row    = current_square.SQUARE_ROW
    final_column = current_square.SQUARE_COLUMN
    password     = 1000 * final_row + 4 * final_column + final_facing
    log(f"RESULTING PASSWORD is {password}.")

    if password != expected_answer_b:
        raise Exception("MISMATCH")

    # log(f"No fails.")


