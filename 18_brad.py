
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

sample_answer_a = 64
sample_answer_b = 58


def log(some_string):
    print(f"P18: {some_string}")


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

    def __init__(self, three_tuple, is_obsidian=False):
        self.VOXEL_TUPLE       = three_tuple
        self.VOXEL_X           = three_tuple[0]
        self.VOXEL_Y           = three_tuple[1]
        self.VOXEL_Z           = three_tuple[2]
        self.VOXEL_IS_OBSIDIAN = is_obsidian

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

    def get_candidate_neighbor_tuples(self, space):
        rv = []
        for delta in self.VOXEL_NEIGHBOR_DELTAS:
            candidate = (
                self.VOXEL_X + delta[0],
                self.VOXEL_Y + delta[1],
                self.VOXEL_Z + delta[2],
              )

            is_good = True
            for ordinal in range(3):
                is_good = is_good and                              \
                    candidate[ordinal] > space.SPACE_MINIMUM and   \
                    candidate[ordinal] < space.SPACE_MAXIMUM
                    
            if is_good: rv.append(candidate)
        return rv

    def voxel_rebirth(self):
       return Voxel(self.VOXEL_TUPLE, self.VOXEL_IS_OBSIDIAN)

    def __str__(self):
        obsidian_string = " OBSIDIAN" if self.VOXEL_IS_OBSIDIAN else ""
        return f"<{self.VOXEL_TUPLE}{obsidian_string}>"



class Space:
    def __init__(self, maximum):
        self.SPACE_MINIMUM = -1
        self.SPACE_MAXIMUM = maximum + 1
        self.__voxels = {}  # ordinate tuple to voxel

    def space_create_acorn(self):
        acorn = self.SPACE_MINIMUM + 1
        return Voxel((acorn, acorn, acorn))

    def space_add(self, new_voxel):
        if new_voxel.VOXEL_TUPLE in self.__voxels: raise Exception("ABuse!")
        self.__voxels[new_voxel.VOXEL_TUPLE] = new_voxel
        return new_voxel

    def space_is_filled(self, candidate_tuple):
        return candidate_tuple in self.__voxels

    def space_is_empty(self, candidate_tuple):
        return not (candidate_tuple in self.__voxels)

    def space_count(self):
        return len(self.__voxels)

    def space_get_voxels(self):
        ordered_tuples = sorted(self.__voxels.keys())
        return [self.__voxels[tpl] for tpl in ordered_tuples]

    def space_get_void_tuples(self):
        rv = []
        for x in range(self.SPACE_MINIMUM + 1, self.SPACE_MAXIMUM):
            for y in range(self.SPACE_MINIMUM + 1, self.SPACE_MAXIMUM):
                for z in range(self.SPACE_MINIMUM + 1, self.SPACE_MAXIMUM):
                    here = (x, y, z)
                    if self.space_is_empty(here):
                        rv.append(here)
        return rv



if __name__ == '__main__':
    if False:
        pure_input = sample_input
        expected_output_part_a = sample_answer_a
        expected_output_part_b = sample_answer_b
        space = Space(7)
    else:
        pure_input = open(DATAFILE, 'r').read()
        expected_output_part_a = 3396
        expected_output_part_b = 2044
        space = Space(20)
    ordinates = parse_input(pure_input)

    log(f"There are {len(ordinates)} tuples.")
    log(f"The second one is {ordinates[1]}")

    simple_voxels = [Voxel(tpl, True) for tpl in ordinates]

    def _do_joining(join_voxels):
        log(f"Doing neighbor association for {len(join_voxels) =} voxels..")
        for voxel_left in join_voxels:
            for voxel_right in join_voxels:
                voxel_left.try_conjoin(voxel_right)
    _do_joining(simple_voxels)

    def _do_show():
        for voxel in simple_voxels:
            log(f"Voxel {voxel} has {voxel.get_neighbor_count()} neighbors")
    _do_show()

    def _do_show_ne():
        for voxel_tuple in (
            (0,  0,  0),
            (20, 20, 20),
            (0,  0,  1),
            (1,  1,  1),
            (2,  2,  2),
          ):
            voxel = Voxel(voxel_tuple)
            log(f"Test flooder {voxel} has {voxel.get_neighbor_count()} neighbors")
            candidate_neigh = voxel.get_candidate_neighbor_tuples(space)
            for neigh in candidate_neigh:
                log(f"    {neigh =}")
    # _do_show_ne()

    def do_chris_calculation(obsidian_voxels):
        total_neighbors = 0
        for voxel in obsidian_voxels:
            total_neighbors += voxel.get_neighbor_count()

        max_possible_surface_area = 6 * len(obsidian_voxels)

        log(f"{max_possible_surface_area = }")
        return max_possible_surface_area - total_neighbors

    part_a_surface_area_answer = do_chris_calculation(simple_voxels)
    log(f"Answer is -> {part_a_surface_area_answer = }")

    if part_a_surface_area_answer != expected_output_part_a:
        raise Exception("WRONG!")

    def _install_obs():
        log(f"Installing obsidian voxels...")

        for voxel in simple_voxels:
            space.space_add(voxel)
    _install_obs()

    def _do_flooding():
        log(f"Before flood, space has {space.space_count() = } elements")
        acorn_voxel = space.space_create_acorn()
        living_voxels = [acorn_voxel]
        while len(living_voxels) > 0:
            new_voxels = []
            for focus_voxel in living_voxels:
                for candidate in focus_voxel.get_candidate_neighbor_tuples(space):
                    if space.space_is_empty(candidate):
                        new_voxels.append(space.space_add(Voxel(candidate)))
            living_voxels = new_voxels
            #log(f"Considering -> {focus_voxel}, living voxels are...")
            #for living_voxel in living_voxels: log(f"     {living_voxel}")
        log(f"After flood, space has {space.space_count() = } elements")
    _do_flooding()

    def _do_peek():
        for peek_voxel in space.space_get_void_tuples():
            log(f"{str(peek_voxel)}")
    # _do_peek()

    second_opinion = do_chris_calculation(simple_voxels)
    log(f"Recap is -> {second_opinion = }")

    filled_tuple  = {}
    for voxel in simple_voxels:
        filled_tuple[voxel.VOXEL_TUPLE] = True
    for tpl in space.space_get_void_tuples():
        filled_tuple[tpl] = True
    
    filled_voxels = [Voxel(tpl) for tpl in filled_tuple.keys()]

    # ugly hack
    _do_joining(filled_voxels)

    part_b_surface_area_answer = do_chris_calculation(filled_voxels)

    log(f"Answer is -> {part_b_surface_area_answer = }")

    if part_b_surface_area_answer != expected_output_part_b:
        raise Exception("WRONG!")

    log(f"SUCCESS!")

