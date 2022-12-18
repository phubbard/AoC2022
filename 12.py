
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
        if from_square.SQUARE_ELEVATION + 1 < to_square.SQUARE_ELEVATION: return False

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
                value = 1 if self.is_traversable(from_instance, to_instance) else 9999999
                current_row.append(value)
            rv.append(tuple(current_row))
        return tuple(rv)


def to_adjacency(map):
    # For each cell/vertex, the LRUD cells are ajdacent if the height difference is <= 1.
    pass



##########################################################
#
#  FROM:  https://www.geeksforgeeks.org/python-program-for-dijkstras-shortest-path-algorithm-greedy-algo-7/
#
#  SUSPECTED FAIL! CUT.
#
#  END
#
##########################################################



##########################################################
#
#  FROM:  https://www.udacity.com/blog/2021/10/implementing-dijkstras-algorithm-in-python.html
#

def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())
 
    # We'll use this dict to save the cost of visiting each node and update it as we move along the graph   
    shortest_path = {}
 
    # We'll use this dict to save the shortest known path to a node found so far
    previous_nodes = {}
 
    # We'll use max_value to initialize the "infinity" value of the unvisited nodes   
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    # However, we initialize the starting node's value with 0   
    shortest_path[start_node] = 0
    
    # The algorithm executes until we visit all nodes
    while unvisited_nodes:
        # The code block below finds the node with the lowest score
        current_min_node = None
        for node in unvisited_nodes: # Iterate over the nodes
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
                
        # The code block below retrieves the current node's neighbors and updates their distances
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node
 
        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)
    
    return previous_nodes, shortest_path

#
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
    if True:
        log(f"show adjacency...")
        for idx, row in enumerate(my_adjacency):
            log(f" {idx:02}: -> {row}")

    if True:
        log(f"Form Graph...")
        graph = Graph(grid.GRID_INSTANCES)
        log(f"Set the Graph's adjacency...")
        graph.adjacency = my_adjacency
        log(f"Locate start and end instances...")
        starting_square = grid.GRID_SQUARES_BY_ORDINATE[start_ordinate[0]][start_ordinate[1]]
        ending_square   = grid.GRID_SQUARES_BY_ORDINATE[end_ordinate[0]][end_ordinate[1]]
        log(f"  The start is instance -> {starting_square.SQUARE_INSTANCE}")
        log(f"  The end   is instance -> {ending_square.SQUARE_INSTANCE}")
        graph.dijkstra(starting_square.SQUARE_INSTANCE, ending_square.SQUARE_INSTANCE)
        log(f"Profit!")
   

