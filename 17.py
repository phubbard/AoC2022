import logging

import numpy
# from tqdm import tqdm
import numpy as np

# The Brad-config
logging.basicConfig(level=logging.DEBUG, format='%(pathname)s(%(lineno)s): %(levelname)s %(message)s')
log = logging.getLogger()

test_winds = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
chamber_width = 7
# np.roll required to place a rock initially
placement_roll = (2, 0)


PLUS = np.array([
    [0, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0]
])
PLUS = np.roll(PLUS, placement_roll)
ELL = np.array([
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0]
])
ELL = np.roll(ELL, placement_roll)
BAR = np.array([
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0]
])
BAR = np.roll(BAR, placement_roll)
HASH = np.array([
    [1, 1, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0]
])
HASH = np.roll(HASH, placement_roll)
MINUS = np.array([
    [1, 1, 1, 1, 0, 0, 0]
])
MINUS = np.roll(MINUS, placement_roll)


class Jet:
    def __init__(self, wind_string):
        self.wind = wind_string
        self.index = 0

    def get(self):
        rc = self.wind[self.index % len(self.wind)]
        self.index += 1
        return rc

    def peek(self):
        return self.wind[self.index]


def display(game_state: np.array):
    # Print out the 7-width grid
    print("game state")
    num_rows = game_state.shape[0]
    for line in range(num_rows):
        rc = ''
        for character in game_state[line]:
            if character == 0:
                rc += ' '
            elif character == 1:
                rc += '#'
            else:
                rc += '!'
        print(rc)


# Get some code running even if its throwaway
def place_rock(rock: numpy.array, game_state: np.array):
    # Add new rocks three rows above current top
    buffer = np.zeros((3, chamber_width))
    new_lines = np.vstack((rock, buffer))
    game_state = np.vstack((new_lines, game_state))
    return game_state



def orchestrate():
    game_state = np.zeros((1, chamber_width))
    winds = Jet(test_winds)
    for cur_rock in [PLUS, ELL, BAR, HASH, MINUS]:
        # Make a copy
        rock = np.array(cur_rock)
        game_state = place_rock(rock, game_state)


    display(game_state)


if __name__ == '__main__':
    orchestrate()
