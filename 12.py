DATAFILE = './data/12.txt'

# Whoa, this takes me back. Some reference pages
# https://en.wikipedia.org/wiki/Dijkstra's_algorithm
# https://en.wikipedia.org/wiki/Adjacency_matrix
# https://www.geeksforgeeks.org/python-program-for-dijkstras-shortest-path-algorithm-greedy-algo-7/


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
            match cell:
                case 'S':
                    start = (row_idx, col_idx,)
                    elevation_map[row_idx].append(0)
                case 'E':
                    end = (row_idx, col_idx,)
                    elevation_map[row_idx].append(to_int('z'))
                case _:
                    elevation_map[row_idx].append(to_int(cell))
            col_idx += 1
        row_idx += 1
    print(f"{start} {end}")
    print(elevation_map)

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
    if (dest_height - source_height) > 1:
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
    print(f"{num_cols} and {num_rows} == {num_cells}")
    # Avert your eyes.
    adj_matrix = [[0 for x in range(num_cells)] for y in range(num_cells)]

    for row_idx in range(num_cells):
        for col_idx in range(num_cells):
            zero_one = is_adjacent(row_idx, col_idx, map)
            adj_matrix[row_idx][col_idx] = zero_one

    return adj_matrix


# Code from https://www.geeksforgeeks.org/python-program-for-dijkstras-shortest-path-algorithm-greedy-algo-7/
# Python program for Dijkstra's single
# source shortest path algorithm. The program is
# for adjacency matrix representation of the graph


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]

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


def rc_to_idx(entry, num_cols):
    return entry[0] * num_cols + entry[1]


if __name__ == '__main__':
    test_to_int()
    # start, end, map = parse_input(test_data.split('\n'))
    start, end, map = parse_input(open(DATAFILE, 'r'))
    a_map = to_adjacency(map)
    g = Graph(len(a_map[0]))
    g.graph = a_map
    num_cols = len(map[0])
    start_idx = rc_to_idx(start, num_cols)
    end_idx = rc_to_idx(end, num_cols)
    distances = g.dijkstra(start_idx)
    print(f"{start_idx} to {end_idx} min distance {distances[end_idx]}")




