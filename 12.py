from copy import deepcopy

DATAFILE = './data/12.txt'

# Whoa, this takes me back. Some reference pages
# https://en.wikipedia.org/wiki/Dijkstra's_algorithm
# https://en.wikipedia.org/wiki/Adjacency_matrix
# https://www.geeksforgeeks.org/python-program-for-dijkstras-shortest-path-algorithm-greedy-algo-7/


def log(some_string):
    print(f"P12: {some_string}")


test_data = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

test_solution = """
v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^
"""

test_move_count = 31


def to_int(input):
    return ord(input) - ord('a')


def test_to_int():
    assert to_int('a') == 0
    assert to_int('z') == 25


def parse_input(data_lines):
    # Return a tuple - start (row, col)
    # end (row, col)
    # 2D elevation map [[]]

    row_count = col_count = 0
    start = tuple()
    end = tuple()
    elevation_map = []

    row_idx = 0
    for line in data_lines:
        if len(line) == 0:
            continue

        elevation_map.append([])
        col_idx = 0
        for cell in line:
            if cell == 'S':
                    start = (row_idx, col_idx, )
                    elevation_map[row_idx].append(0)
            elif cell == 'E':
                    end = (row_idx, col_idx, )
                    elevation_map[row_idx].append(to_int('z'))
            else:
                    elevation_map[row_idx].append(to_int(cell))
            col_idx += 1
        row_idx += 1
    print(f"start {start} end {end}")
    # print(elevation_map)

    return start, end, elevation_map


def is_adjacent(source: int, dest: int, elevation_map) -> int:
    # The adjacency matrix creation needs to know if two vertices are connected or not. This answers it.
    num_cols = len(elevation_map[0])
    source_row, source_col = divmod(source, num_cols)
    dest_row, dest_col = divmod(dest, num_cols)
    source_height = elevation_map[source_row][source_col]
    dest_height = elevation_map[dest_row][dest_col]

    if source == dest:
        return 0  # Zeros on the diagonal by definition
    # For part one, you can step up one or down many. For part two, only up or down one.
    # if (dest_height - source_height) > 1:
    if (source_height - dest_height) > 1:
        return 0

    if source_row == dest_row:
        if abs(source_col - dest_col) > 1:
            return 0  # More than one away
        # nb we already checked for height diff above
        return 1
    if abs(source_row - dest_row) > 1:
        return 0
    if source_col == dest_col:
        return 1

    # All that and checking delta H and distance might be a lot simpler. Ahh well.
    return 0


def to_adjacency(map):
    # For each cell/vertex, the LRUD cells are adjacent if the height difference is <= 1.
    # For N cells, the matrix is NxN, symmetric about the diagonal, zeros on diagonal
    num_cols = len(map[0])
    col_zero = [row[0] for row in map]
    num_rows = len(col_zero)
    num_cells = num_rows * num_cols
    print(f"{num_cols} cols and {num_rows} rows == {num_cells}^2 in adjacency matrix")
    # Avert your eyes.
    zero_row = [0 for x in range(num_cells)]
    adj_matrix = [deepcopy(zero_row) for y in range(num_cells)]

    for row_idx in range(num_cells):
        for col_idx in range(num_cells):
            adj_matrix[row_idx][col_idx] = is_adjacent(row_idx, col_idx, map)

    return adj_matrix


##########################################################
#
# Code from https://www.geeksforgeeks.org/python-program-for-dijkstras-shortest-path-algorithm-greedy-algo-7/

class Graph:
    # Code from https://www.geeksforgeeks.org/python-program-for-dijkstras-shortest-path-algorithm-greedy-algo-7/
    # Python program for Dijkstra's single source shortest path algorithm. The program is
    # for adjacency matrix representation of the graph.
    def __init__(self, vertices):
        self.V = len(vertices[0])
        self.graph = vertices

    def printSolution(self, dist):
        print("Vertex \t Distance from Source")
        for node in range(self.V):
            print(node, "\t\t", dist[node])

    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minDistance(self, dist, sptSet):

        # Initialize minimum distance for next node
        min = 1e7

        # Search not nearest vertex not in the
        # shortest path tree
        min_index = 0
        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v

        return min_index

    # Function that implements Dijkstra's single source
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation
    def dijkstra(self, src):

        dist = [1e7] * self.V
        dist[src] = 0
        sptSet = [False] * self.V

        for cout in range(self.V):

            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
            u = self.minDistance(dist, sptSet)

            # Put the minimum distance vertex in the
            # shortest path tree
            sptSet[u] = True

            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            for v in range(self.V):
                if (self.graph[u][v] > 0 and
                        sptSet[v] == False and
                        dist[v] > dist[u] + self.graph[u][v]):
                    dist[v] = dist[u] + self.graph[u][v]

        # self.printSolution(dist)
        return dist

# This code is contributed by Divyanshu Mehta

#  END
#
##########################################################


class Square:

    __slots__ = ('SQUARE_INSTANCE', 'SQUARE_X', 'SQUARE_Y', 'SQUARE_ELEVATION')

    def __init__(self, instance, x, y, elevation):
        self.SQUARE_INSTANCE  = instance
        self.SQUARE_X         = x
        self.SQUARE_Y         = y
        self.SQUARE_ELEVATION = elevation


class Grid:
    def __init__(self, two_d_array_of_elevations):
        squares_by_instance = []
        squares_by_ordinate = []
        max_x = 0
        max_y = 0
        for y, row in enumerate(two_d_array_of_elevations):
            current_row = []
            for x, elevation in enumerate(row):
                new_square = Square(len(squares_by_instance), x, y, elevation)
                squares_by_instance.append(new_square)
                current_row.append(new_square)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
            squares_by_ordinate.append(tuple(current_row))

        self.GRID_SQUARES_BY_INSTANCE = tuple(squares_by_instance)
        self.GRID_SQUARES_BY_ORDINATE = tuple(squares_by_ordinate)
        self.GRID_INSTANCES           = len(self.GRID_SQUARES_BY_INSTANCE)
        self.GRID_X_EXTENT            = max_x
        self.GRID_Y_EXTENT            = max_y

    def is_traversable(self, from_instance: int, to_instance: int) -> bool:
        from_square = self.GRID_SQUARES_BY_INSTANCE[from_instance]
        to_square   = self.GRID_SQUARES_BY_INSTANCE[to_instance]

        if from_square == to_square: return False
        if to_square.SQUARE_ELEVATION + 1 < from_square.SQUARE_ELEVATION: return False

        if abs(from_square.SQUARE_X - to_square.SQUARE_X) > 1: return False
        if abs(from_square.SQUARE_Y - to_square.SQUARE_Y) > 1: return False

        if from_square.SQUARE_X == to_square.SQUARE_X: return True
        if from_square.SQUARE_Y == to_square.SQUARE_Y: return True

        return False

    def create_adjacency_matrix(self):
        rv = []
        for from_instance in range(self.GRID_INSTANCES):
            current_row = []
            for to_instance in range(self.GRID_INSTANCES):
                value = 1 if self.is_traversable(from_instance, to_instance) else 0
                current_row.append(value)
            rv.append(current_row)
        return rv



def rc_to_idx(entry, num_cols):
    return entry[0] * num_cols + entry[1]


if True:
    log(f"Parse input...")
    start_ordinate, end_ordinate, two_dee_array = parse_input(test_data.split('\n'))
    log(f"Form the grid...")
    grid = Grid(two_dee_array)
    log(f"Get adjacency...")
    my_adjacency = grid.create_adjacency_matrix()

    if True:
        log(f"Form Graph...")
        my_graph = Graph(my_adjacency)
        log(f"Locate start and end instances...")
        starting_square = grid.GRID_SQUARES_BY_ORDINATE[start_ordinate[0]][start_ordinate[1]]
        ending_square   = grid.GRID_SQUARES_BY_ORDINATE[end_ordinate[0]][end_ordinate[1]]
        log(f"  The start is instance -> {starting_square.SQUARE_INSTANCE}")
        log(f"  The end   is instance -> {ending_square.SQUARE_INSTANCE}")
        solution_array = my_graph.dijkstra(ending_square.SQUARE_INSTANCE)
        log(f"Solutions are -> {solution_array}")
        log(f"Key solution is -> {solution_array[starting_square.SQUARE_INSTANCE]}")
        log(f"Profit!")


if __name__ == '__main__':
    test_to_int()
    # start, end, map = parse_input(test_data.split('\n'))
    # for row in map:
    #     print(row)

    start, end, map = parse_input(open(DATAFILE, 'r'))
    a_map = to_adjacency(map)
    g = Graph(a_map)
    num_src_cols = len(map[0])
    start_idx = rc_to_idx(start, num_src_cols)
    end_idx = rc_to_idx(end, num_src_cols)
    print(f"Starting from the end for part two - {end_idx}")
    distances = g.dijkstra(end_idx)
    print(f"Double check - {distances[start_idx]}")
    # We now have an array of vertex, distance pairs, starting from the end index. Now we need to augment that
    # with elevation data.
    idx = 0   # FIXME RTFM for the index, value trick
    fewest_steps = 999999
    for path_length in distances:
        row1, col1 = divmod(idx, num_src_cols)
        result = row1, col1
        row, col = result
        height = map[row][col]
        if height == 0:
            if path_length < fewest_steps:
                fewest_steps = path_length
        idx += 1
    print(f"Min path length {fewest_steps}")




