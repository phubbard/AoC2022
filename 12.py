
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
    print(f"{start} {end}")
    print(elevation_map)

    return(start, end, elevation_map)


class Square:

    __slots__ = ('SQ_INSTANCE', 'SQ_X', 'SQ_Y', 'SQ_ELEVATION')

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
        if abs(from_square.SQUARE_X - to_square.SQUARE_X) > 1: return False
        if abs(from_square.SQUARE_Y - to_square.SQUARE_Y) > 1: return False
        if from_square.SQUARE_ELEVATION + 1 < to_square.SQUARE_ELEVATION: return False

        return True

    def create_adjacency_matrix(self):
        rv = []
        for from_instance in range(self.GRID_INSTANCES):
            current_row = []
            for to_instance in range(self.GRID_INSTANCES):
                value = 1 if self.is_traversable(from_instance, to_instance) else 0
                current_row[to_instance] = value
            rv.append(tuple(current_row))
        return tuple(rv)


def to_adjacency(map):
    # For each cell/vertex, the LRUD cells are ajdacent if the height difference is <= 1.
    pass



##########################################################
#
#  FROM:  https://www.geeksforgeeks.org/python-program-for-dijkstras-shortest-path-algorithm-greedy-algo-7/

# Python program for Dijkstra's single
# source shortest path algorithm. The program is
# for adjacency matrix representation of the graph
class Graph():

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

		self.printSolution(dist)

# Driver program
def test_algorithm():
    g = Graph(9)
    g.graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
    		[4, 0, 8, 0, 0, 0, 0, 11, 0],
    		[0, 8, 0, 7, 0, 4, 0, 0, 2],
    		[0, 0, 7, 0, 9, 14, 0, 0, 0],
    		[0, 0, 0, 9, 0, 10, 0, 0, 0],
    		[0, 0, 4, 14, 10, 0, 2, 0, 0],
    		[0, 0, 0, 0, 0, 2, 0, 1, 6],
    		[8, 11, 0, 0, 0, 0, 1, 0, 7],
    		[0, 0, 2, 0, 0, 0, 6, 7, 0]
    		]
    g.dijkstra(0)

# This code is contributed by Divyanshu Mehta


#  END
#
##########################################################


if __name__ == '__main__':
    log("Run test...")
    test_to_int()
    log(f"Parse input...")
    start_ordinate, end_ordinate, two_dee_array = parse_input(test_data.split('\n'))
    log(f"Form the grid...")
    grid = Grid(two_dee_array)
    log(f"Get adjacency...")
    my_adjacency = grid.create_adjacency_matrix()
    log(f"Form Graph...")
    graph = Graph(grid.GRID_INSTANCES)
    log(f"Set the Graph's adjacency...")
    graph.adjacency = my_adjacency
    log(f"Locate start and end instances...")
    starting_square = grid.GRID_SQUARES_BY_ORDINATE[start_ordinate[0]][start_ordinate[1]]
    ending_square   = grid.GRID_SQUARES_BY_ORDINATE[end_ordinate[0]][end_ordinate[1]]
    log(f"  The start is instance -> {starting_square.SQUARE_INSTANCE}")
    log(f"  The end   is instance -> {ending_square.SQUARE_INSTANCE}")
    g.dijkstra(starting_square.SQUARE_INSTANCE)
    log(f"Profit!")
   

