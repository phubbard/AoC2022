
import collections


DATAFILE = "./data/16.txt"

sample_input = """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""

sample_answer = 1651


def log(some_string):
    print(f"P16: {some_string}")


def parse_input(data_lines):
    lines = data_lines.strip()
    names   = []
    flows   = []
    tunnels = []
    for line in lines.split("\n"):
        line = line.replace("Valve ", "")
        line = line.replace("valves", "valve")
        first_split  = line.split(" has flow rate=")
        second_split = first_split[1].split(";")
        third_split  = second_split[1].split("valve ")
        fourth_split = third_split[1].strip().split(", ") 

        names.append(first_split[0])
        flows.append(int(second_split[0]))
        tunnels.append(tuple(fourth_split))

    return names, flows, tunnels

##########################################################
#

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
        log(f"Starting dijkstra from {src}...")

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
        return dist

# This code is contributed by Divyanshu Mehta

#  END
#
##########################################################


class Valve:
    def __init__(self, instance, name, flow):
        self.VALVE_INSTANCE = instance
        self.VALVE_NAME     = name
        self.VALVE_FLOW     = flow

    def name_if_key(self):
        if self.VALVE_FLOW > 0 or self.VALVE_NAME == 'AA':
            return self.VALVE_NAME
        return ""


class Network:
    def __init__(self):
        self.__instance = 0
        self.__valves = collections.OrderedDict()

    def add_valve(self, name, flow):
        valve = Valve(self.__instance, name, flow)
        self.__instance += 1
        if name in self.__valves: raise Exception(f"dupes")
        self.__valves[name] = valve

    def freeze_valves(self):
        self.__full_adjacency = [([0] * self.__instance) for _ in range(self.__instance)]

    def add_tunnel(self, name_source, name_destination):
        index_source      = self.__valves[name_source].VALVE_INSTANCE
        index_destination = self.__valves[name_destination].VALVE_INSTANCE
        self.__full_adjacency[index_source][index_destination] = 1

    def show(self):
        row = "    "
        for valve in self.__valves.values():
            row += f" {valve.VALVE_NAME}"
        log(row)

        for valve in self.__valves.values():
            row = f" {valve.VALVE_NAME}:"
            for column in self.__full_adjacency[valve.VALVE_INSTANCE]:
                row += f" {column:2}"
            log(row)

    def static_show(self, labels, matrix):
        """Technically static."""
        longest = 0
        row = " "
        for label in labels:
            if len(label) == 0: continue
            longest = max(longest, len(label))
            row += f" {label}"
        log(f"{' ' * longest} {row}")

        for row_instance, label in enumerate(labels):
            if len(label) == 0: continue
            row = f" {label:2}:"
            for column_instance, column in enumerate(matrix[row_instance]):
                if len(labels[column_instance]) == 0: continue
                row += f" {column:2}"
            log(row)

    def better_show(self):
        self.static_show([valve.VALVE_NAME for valve in self.__valves.values()], self.__full_adjacency)

    def create(self):
        """ Create the adjsacency matrix eliminating unusable flows."""

        mini_adjacency = []
        for index_from, valve_from in enumerate(self.__valves.values()):
            graph = Graph(self.__full_adjacency)
            paths = graph.dijkstra(valve_from.VALVE_INSTANCE)
            current_row = []
            for index_to, valve_to in enumerate(self.__valves.values()):
                current_row.append(paths[index_to])
            mini_adjacency.append(current_row)

        mini_list = [valve.name_if_key() for valve in self.__valves.values()]

        self.static_show(mini_list, mini_adjacency)




if __name__ == '__main__':
    if False:
        pure_input = sample_input
    else:
        pure_input = open(DATAFILE, 'r').read()

    names, flows, tunnels = parse_input(pure_input)

    network = Network()
    for instance, name in enumerate(names):
        network.add_valve(name, flows[instance])

    network.freeze_valves()
    for instance, name in enumerate(names):
        tunnel_tuple = tunnels[instance]
        for tunnel in tunnel_tuple:
            network.add_tunnel(name, tunnel)

    network.show()
    network.better_show()

    network.create()

    log(f"SUCCESS")


