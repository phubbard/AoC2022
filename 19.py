from dataclasses import dataclass
import re

sample_input = """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"""
sample_answers = [9, 12]
DATAFILE = './data/19.txt'
pattern = r'\d+'
matcher = re.compile(pattern)


@dataclass
class Blueprint:
    index: int
    ore_cost: int
    clay_cost: int
    obsidian_cost: (int, int)
    geode_cost: (int, int)


def parse_data(data_lines):
    rc = []
    for index, line in enumerate(data_lines):
        groups = matcher.findall(line)
        if not groups:
            continue
        bp = Blueprint(int(groups[0]), int(groups[1]), int(groups[2]), (int(groups[3]), int(groups[4])),
                       (int(groups[5]), int(groups[6])))
        rc.append(bp)

    return rc


def orchestrate():
    data = parse_data(sample_input.split('\n'))
    # big_data = parse_data(open(DATAFILE, 'r'))

    for blueprint in data:
        time = 1
        ore_bots = 1
        clay_bots = 0
        obsidian_bots = 0
        geode_bots = 0
        ore_count = 0
        clay_count = 0
        obsidian_count = 0
        geode_count = 0

        while time < 25:
            new_ore_bots = new_clay_bots = new_obsidian_bots = new_geode_bots = 0

            # Do we have enough ore and obsidian to make a geode bot?
            if ore_count >= blueprint.geode_cost[0] and obsidian_count >= blueprint.geode_cost[1]:
                new_geode_bots += 1
                ore_count -= blueprint.geode_cost[0]
                obsidian_count -= blueprint.geode_cost[1]
            # Do we have enough ore and clay to make an obsidian bot?
            if ore_count >= blueprint.obsidian_cost[0] and clay_count >= blueprint.obsidian_cost[1]:
                new_obsidian_bots += 1
                ore_count -= blueprint.obsidian_cost[0]
                clay_count -= blueprint.obsidian_cost[1]
            # Enough ore to make a clay bot?
            if ore_count >= blueprint.clay_cost:
                new_clay_bots += 1
                ore_count -= blueprint.clay_cost

            # Existing bots do their mining
            ore_count += ore_bots
            clay_count += clay_bots
            obsidian_count += obsidian_bots
            geode_count += geode_bots

            # Bots created this minute cannot mine yet
            ore_bots += new_ore_bots
            clay_bots += new_clay_bots
            obsidian_bots += new_obsidian_bots
            geode_bots += new_geode_bots
            
            print(f'{time=} {ore_count=} {clay_count=} {obsidian_count=} {geode_count=} {ore_bots=} {clay_bots=} {obsidian_bots=} {geode_bots =}')
            time += 1
        print(
            f'Done {blueprint.index=} {geode_count=} {ore_count=} {clay_count=} {obsidian_count=} {ore_bots=} {clay_bots=} {obsidian_bots=} {geode_bots =}')


if __name__ == '__main__':
    orchestrate()
