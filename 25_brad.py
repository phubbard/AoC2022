
DATAFILE = './data/25.txt'

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
sample_answer_a = "2=-1=0"



test_nums_alt = [
        (         1,              "1"),
        (         2,              "2"),
        (         3,             "1="),
        (         4,             "1-"),
        (         5,             "10"),
        (         6,             "11"),
        (         7,             "12"),
        (         8,             "2="),
        (         9,             "2-"),
        (        10,             "20"),
        (        15,            "1=0"),
        (        20,            "1-0"),
        (      2022,         "1=11-2"),
        (     12345,        "1-0---0"),
        ( 314159265,  "1121-1110-1=0"),
    ]



def log(some_string):
    print(f"P25: {some_string}")


# From https://stackoverflow.com/questions/2267362/how-to-convert-an-integer-to-a-string-in-any-base
def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


def base_5_array_to_snafu_array(b5_array):
    safe_array = [0] + [x for x in b5_array]
    safe_array.reverse()

    log(f"{safe_array=}")
    rv_array = []
    for idx in range(len(safe_array)):
        digit = safe_array[idx]
        if digit == 3:
            safe_array[idx + 1] += 1
            digit = '='
        elif digit == 4:
            safe_array[idx + 1] += 1
            digit = '-'
        elif digit == 5:
            safe_array[idx + 1] += 1
            digit = '0'
        else:
            digit = str(digit)
        rv_array.append(digit)

    if rv_array[-1] == '0':
        rv_array.pop()

    rv_array.reverse()

    return rv_array


def dec_to_sn(decimal: int) -> str:
    as_base_5_array = numberToBase(decimal, 5)
    my_snafu = ''.join(base_5_array_to_snafu_array(as_base_5_array))
    return my_snafu


if __name__ == '__main__':

    do_sample = True

    if do_sample:
        pure_input        = sample_data
        expected_answer_a = sample_answer_a
    else:
        pure_input        = open(DATAFILE, 'r').read()
        expected_answer_a = -1

    for dec, snafu in test_nums_alt:
        log(f"")

        as_base_5_array = numberToBase(dec, 5)
        b5 = ''.join([str(x) for x in as_base_5_array])

        my_snafu = ''.join(base_5_array_to_snafu_array(as_base_5_array))

        my_better_snafu = dec_to_sn(dec)

        log(f" {dec} {snafu:>10}")
        log(f" {dec} {my_snafu:>10}")
        assert my_better_snafu == snafu

    log("No failures.")


