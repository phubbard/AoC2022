from collections import deque

sample_data = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""

DATAFILE = './data/25.txt'

test_nums = """
  Decimal          SNAFU
        1              1
        2              2
        3             1=
        4             1-
        5             10
        6             11
        7             12
        8             2=
        9             2-
       10             20
       15            1=0
       20            1-0
     2022         1=11-2
    12345        1-0---0
314159265  1121-1110-1=0
"""
snd_nums = """
 SNAFU  Decimal
1=-0-2     1747
 12111      906
  2=0=      198
    21       11
  2=01      201
   111       31
 20012     1257
   112       32
 1=-1=      353
  1-12      107
    12        7
    1=        3
   122       37
"""
sample_sum = 4890

sd_test = [
    ['1=-0-2', 1747],
    ['12111', 906],
    ['2=0=', 198],
    ['21', 11],
    ['2=01', 201],
    ['111', 31],
    ['20012', 1257],
    ['112', 32],
    ['1=-1=', 353],
    ['1-12', 107],
    ['12', 7],
    ['1=', 3],
    ['122', 37],
]

sn_test = [
    [1, '1'],
    [2, '2'],
    [3, '1='],
    [4, '1-'],
    [5, '10'],
    [6, '11'],
    [7, '12'],
    [8, '2='],
    [9, '2-'],
    [10, '20'],
    [15, '1=0'],
    [20, '1-0'],
    [2022, '1=11-2'],
    [12345, '1-0---0'],
    [314159265, '1121-1110-1=0']
]


def clean_data_lines(data_lines):
    # Blank lines throw off the parsing and indexing; this drops them
    return [x for x in data_lines if len(x) > 0]


def parse_input(data_lines):
    data_lines = clean_data_lines(data_lines)
    return [x.strip() for x in data_lines]


def try_base_conversion():
    for entry in sn_test:
        print(f'{entry=}')
        assert (sn_to_dec(entry[1]) == entry[0])
        assert (dec_to_sn(entry[0]) == entry[1])

    for entry in sd_test:
        print(f'{entry=}')
        assert sn_to_dec(entry[0]) == entry[1]
        assert dec_to_sn(entry[1]) == entry[0]


def dec_to_sn(decimal: int) -> str:
    return ''


def sn_to_dec(snafu: str) -> int:
    sn_lookup = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
    cur_power = (len(snafu) - 1)
    sn_deque = deque(snafu)
    running_sum = 0
    cur_character = sn_deque.popleft()
    while cur_character:
        running_sum += sn_lookup[cur_character] * 5 ** cur_power
        cur_character = sn_deque.popleft() if len(sn_deque) > 0 else None
        cur_power -= 1
    return running_sum


if __name__ == '__main__':
    # try_base_conversion()
    if False:
        snafus = parse_input(sample_data.split('\n'))
    else:
        snafus = parse_input(open(DATAFILE, 'r').read().split('\n'))
    answer = sum([sn_to_dec(x) for x in snafus])
    print(f'{answer=:,} {dec_to_sn(answer)=}')