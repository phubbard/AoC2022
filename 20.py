
from copy import deepcopy
from collections import deque

sample_input = """1
2
-3
3
-2
0
4"""
DATAFILE = './data/20.txt'
# Data as deques of (index, value) pairs
original_sample = list(map(int, sample_input.split('\n')))
full_data = list(map(int, open(DATAFILE, 'r').readlines()))

# part two
decryption_key = 811589153


def mix(enumerated: deque):
    """ Perform the mix algorithm on our enumerated deque of numbers """
    # Move each number once, using original indexes
    # We can't iterate over actual values from enumerated, since we'll be modifying it as we go
    for original_index in range(len(enumerated)):
        while enumerated[0][0] != original_index:  # bring our required element to the left end
            enumerated.rotate(-1)

        current_pair = enumerated.popleft()
        shift = current_pair[1] % len(enumerated)  # retrieve the value to move by; allow for wrapping over
        enumerated.rotate(-shift)  # rotate everything by n positions
        enumerated.append(current_pair)  # and now reinsert our pair at the end

    return enumerated


def value_at_n(values: list, n: int):
    """ Determine the value at position n in our list.
    If index is beyond the end, then wrap the values as many times as required. """
    digit_posn = (values.index(0)+n) % len(values)
    return values[digit_posn]


if __name__ == '__main__':
    # deque of tuples of (original index, value
    enumerated = deque(list(enumerate(full_data.copy())))
    mixed_sequence = mix(enumerated)
    coordinate_sum = 0
    for index in [1000, 2000, 3000]:
        coordinate_sum += value_at_n([val[1] for val in enumerated], index)
    print(f"{coordinate_sum=}")

    p2_data = [x * decryption_key for x in full_data]
    enumerated = deque(list(enumerate(p2_data)))
    for _ in range(10):
        enumerated = mix(enumerated)
    coordinate_sum = 0
    for index in [1000, 2000, 3000]:
        coordinate_sum += value_at_n([val[1] for val in enumerated], index)
    print(f"part two {coordinate_sum=}")
