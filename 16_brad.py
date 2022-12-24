
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


class Valve:
    def __init__(self, instance, name, flow):
        self.VALVE_INSTANCE = instance
        self.VALVE_NAME     = name
        self.VALVE_FLOW     = flow


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


if __name__ == '__main__':
    if True:
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

    # g = Graph(a_map)
    log(f"SUCCESS")


