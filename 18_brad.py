
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


class Voxel:

    VOXEL_NEIGHBOR_DELTAS = [
        (+0, +0, -1, ),
        (+0, +0, +1, ),
        (+0, -1, +0, ),
        (+0, +1, +0, ),
        (-1, +0, +0, ),
        (+1, +0, +0, ),
     ]

    def __init__(self, three_tuple):
        self.VOXEL_TUPLE = three_tuple
        self.VOXEL_X     = three_tuple[0]
        self.VOXEL_Y     = three_tuple[1]
        self.VOXEL_Z     = three_tuple[2]

        self.__neighbors = collections.OrderedDict() # Voxel to True

    def try_conjoin(self, other_voxel):
        delta_tuple = (
            self.VOXEL_X - other_voxel.VOXEL_X, 
            self.VOXEL_Y - other_voxel.VOXEL_Y, 
            self.VOXEL_Z - other_voxel.VOXEL_Z,
          )

        if delta_tuple in self.VOXEL_NEIGHBOR_DELTAS:
            self.__neighbors[other_voxel] = True
            other_voxel.__neighbors[self] = True

        return

    def get_neighbor_count(self):
        return len(self.__neighbors)

    def __str__(self):
        return f"({self.VOXEL_TUPLE})"


if __name__ == '__main__':
    if True:
        pure_input = sample_input
        expected_output = sample_answer
    else:
        pure_input = open(DATAFILE, 'r').read()
        expected_output = -1
    ordinates = parse_input(pure_input)

    log(f"There are {len(ordinates)} tuples.")
    log(f"The second one is {ordinates[1]}")

    simple_voxels = [Voxel(tpl) for tpl in ordinates]

    def _do_joining():
        for voxel_left in simple_voxels:
            for voxel_right in simple_voxels:
                voxel_left.try_conjoin(voxel_right)
    _do_joining()

    for voxel in simple_voxels:
        log(f"Voxel {voxel} has {voxel.get_neighbor_count()} neighbors")

    log(f"SUCCESS")

