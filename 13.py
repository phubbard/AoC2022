
# Problem spec https://adventofcode.com/2022/day/13
DATAFILE = "./data/13.txt"

sample_data = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""

sample_answers = [True, True, False, True, False, True, False, False]


def is_list(item:str) -> bool:
    # TODO verify that this suffices!
    return not item.isnumeric()


def compare_pair(left:str, right:str) -> bool:
    # Returns true if in correct order, false if wrong order, None if undecidable
    if left.isnumeric() and right.isnumeric():
        if int(left) < int(right):
            return True
        if int(right) > int(left):
            return False
        # They're equal - proceed
        # TODO
    if is_list(left) and is_list(right):
        # TODO pairwise compare with rules about shorter list as per doc

    if left.isnumeric() and is_list(right):
        return compare_pair([left], right)


