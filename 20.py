
from collections import deque

sample_input = """1
2
-3
3
-2
0
4"""
DATAFILE = './data/20.txt'
original_sequence = [int(x.strip()) for x in sample_input.split('\n')]
data = [int(x.strip()) for x in open(DATAFILE, 'r').readlines()]


def deque_remove(input_data: list, index: int) -> deque:
    # Return a deque with the element at index dropped
    rc = deque(input_data[0:index])
    rc.extend(input_data[index + 1:])
    return rc


def deque_mix(sequence: list):
    rc = deque(sequence)
    for index, value in enumerate(sequence):
        current_index = rc.index(value)
        new_index = (current_index + value) % len(sequence)
        if value < 0:
            new_index -= 1
        rc = deque_remove(list(rc), current_index)
        rc.insert(new_index, value)
    return rc


def orchestrate():
    mixed_sequence = deque_mix(original_sequence)
    coordinate_sum = 0
    zero_index = mixed_sequence.index(0)
    for index in [1000, 2000, 3000]:
        value_index = (zero_index + index) % len(mixed_sequence)
        temp = mixed_sequence[value_index]
        coordinate_sum += temp
    tfstr = 'correct' if coordinate_sum == 3 else 'incorrect'
    print(f'sample data {coordinate_sum=} {tfstr}')

    mixed_sequence = deque_mix(data)
    coordinate_sum = 0
    zero_index = mixed_sequence.index(0)
    for index in [1000, 2000, 3000]:
        value_index = (zero_index + index) % len(mixed_sequence)
        temp = mixed_sequence[value_index]
        coordinate_sum += temp
    print(f'Data {coordinate_sum=}')


if __name__ == '__main__':
    orchestrate()