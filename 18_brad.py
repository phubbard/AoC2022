
import collections

DATAFILE = "./data/18.txt"

sample_input = """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""

sample_answer = 64


def log(some_string):
    print(f"P16: {some_string}")


def parse_input(data_lines):
    lines = data_lines.strip()
    rv = []
    for line in lines.split("\n"):
        ordinate = eval(f"({line})")
        rv.append(ordinate)
    return rv



if __name__ == '__main__':
    if False:
        pure_input = sample_input
        expected_output = sample_answer
    else:
        pure_input = open(DATAFILE, 'r').read()
        expected_output = -1
    ordinates = parse_input(pure_input)

    log(f"There are {len(ordinates)} tuples.")
    log(f"The second one is {ordinates[1]}")
    log(f"SUCCESS")


