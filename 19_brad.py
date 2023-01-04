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
        bp = Blueprint(int(groups[0]), int(groups[1]), int(groups[2]), (int(groups[3]), int(groups[4])), (int(groups[5]), int(groups[6])))
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


if False:
    orchestrate()


def log(some_string):
    print(f"P19: {some_string}")


class Ruple:
    def __init__(self, ore, clay, obsidian, geode):
        self.RUPLE_ORE      = ore
        self.RUPLE_CLAY     = clay
        self.RUPLE_OBSIDIAN = obsidian
        self.RUPLE_GEODE    = geode

    def ruple_add(self, ruple_other):
        rv = Ruple(self.RUPLE_ORE      + ruple_other.RUPLE_ORE,
                   self.RUPLE_CLAY     + ruple_other.RUPLE_CLAY,
                   self.RUPLE_OBSIDIAN + ruple_other.RUPLE_OBSIDIAN,
                   self.RUPLE_GEODE    + ruple_other.RUPLE_GEODE)
        return rv

    def is_viable(self):
        rv = True                      \
            and rv.RUPLE_ORE      > 0  \
            and rv.RUPLE_CLAY     > 0  \
            and rv.RUPLE_OBSIDIAN > 0  \
            and rv.RUPLE_GEODE    > 0
        return rv

    def ruple_minus(self, ruple_other):
        rv = Ruple(self.RUPLE_ORE      - ruple_other.RUPLE_ORE,
                   self.RUPLE_CLAY     - ruple_other.RUPLE_CLAY,
                   self.RUPLE_OBSIDIAN - ruple_other.RUPLE_OBSIDIAN,
                   self.RUPLE_GEODE    - ruple_other.RUPLE_GEODE)
        return rv

    def ruple_engulfs(self, ruple_other):
        if self.RUPLE_ORE      < ruple_other.RUPLE_ORE:      return False
        if self.RUPLE_CLAY     < ruple_other.RUPLE_CLAY:     return False
        if self.RUPLE_OBSIDIAN < ruple_other.RUPLE_OBSIDIAN: return False
        if self.RUPLE_GEODE    < ruple_other.RUPLE_GEODE:    return False
        return True

    def __str__(self):
        return f"({self.RUPLE_ORE}, {self.RUPLE_CLAY}, {self.RUPLE_OBSIDIAN}, {self.RUPLE_GEODE})"

# N,R,L,B,E




#################
#  Well this is a stall.  What next?  Lets journal on this.  
#  
#  So, right now I'm musing the optimization question of, what is the fastest I can crack
#  N geodes in?  It is not clear to me that there's a strong relationship between N and N + 1
#  in this treatment.  But there could be, and should be.  Pretty close, honestly.  The
#  sequences ought not diverge too much.  Hmm but I don't have a good shuffle either, i.e. given
#  a sequence, what is another set of similar sequences?  
#  
#  Okay, I'm going to anchor on a different problem.  Given a number of Geodes, what is the
#  fastest way to get to that number?  Does that actually tell us anything?
#
#  Well it might...
#  
#  Okay I've second guessed that to smithereens.  Crud.  Okay, next thought, is there a 'similarity'
#  between two different 'genomes' such that I can generate a permutation field against one and figure
#  out if there are better things nearby?  Minimize secondary resources, maximize geodes.  Hmm, the
#  gene permuters are... add a 'space' in the middle, remove a 'space',  add a creation, delete a
#  creation.  How many are there likely to be?  How good is the fitness function?
#  
#  HAH, I like this one.  Picture the 'genome' as simply the ordered list of which robot to
#  create next.  This leads directly to a number of resources at any given time.  Huh.  Highly
#  dynamic.  Yep there it is.  
#  

ACTION_ORE      = 'ore'
ACTION_CLAY     = 'clay'
ACTION_OBSIDIAN = 'obsidian'
ACTION_GEODE    = 'geode'

class Fact:
    def __init__(self, genome, minute, robot_ruple, resource_total_ruple, resource_addition_ruple):
        self.FACT_GENOME                  = genome
        self.FACT_MINUTE                  = minute
        self.FACT_ROBOT_RUPLE             = robot_ruple
        self.FACT_RESOURCE_TOTAL_RUPLE    = resource_total_ruple
        self.FACT_RESOURCE_ADDITION_RUPLE = resource_addition_ruple

    def fact_feed_forward(self, new_genome, resource_threshold_ruple, delta_robot_ruple):

        # Cannot do anything if we never add these
        if resource_threshold_ruple.RUPLE_CLAY     > 0 and self.FACT_RESOURCE_ADDITION_RUPLE.RUPLE_CLAY     == 0: return None
        if resource_threshold_ruple.RUPLE_OBSIDIAN > 0 and self.FACT_RESOURCE_ADDITION_RUPLE.RUPLE_OBSIDIAN == 0: return None

        # Addition will eventually enable changes
        minutes = self.FACT_MINUTE
        next_total_ruple = self.FACT_RESOURCE_TOTAL_RUPLE
        while True:
            if minutes > 300: raise Exception("FATAL GROISSS")
            # log(f" Checking if {str(next_total_ruple)} engulfs {str(resource_threshold_ruple)}")
            if next_total_ruple.ruple_engulfs(resource_threshold_ruple):
                break
            minutes += 1
            next_total_ruple = next_total_ruple.ruple_add(self.FACT_RESOURCE_ADDITION_RUPLE)

        # Return next
        return Fact(new_genome,
                    minutes,
                    self.FACT_ROBOT_RUPLE.ruple_add(delta_robot_ruple),
                    next_total_ruple.ruple_minus(resource_threshold_ruple),
                    self.FACT_RESOURCE_ADDITION_RUPLE.ruple_add(delta_robot_ruple))

    def __str__(self):
        return f"[FACT minute:{self.FACT_MINUTE} with robots {self.FACT_ROBOT_RUPLE} and resources {self.FACT_RESOURCE_TOTAL_RUPLE} from {self.FACT_GENOME} ]"


class Genome:
    def __init__(self, decision_list):
        self.GENOME_DECISION_LIST = [decision for decision in decision_list]

    def genome_factory(self, next_action):
        rv = [decision for decision in self.GENOME_DECISION_LIST]
        rv.append(next_action)
        return Genome(rv)

    def __str__(self):
        meat = '-'.join(self.GENOME_DECISION_LIST)
        return f"(GENOME {meat})"


class Oracle:

    ALL_ACTIONS = [ ACTION_ORE, ACTION_CLAY, ACTION_OBSIDIAN, ACTION_GEODE ]

    ZERO_RUPLE = Ruple(0, 0, 0, 0)
    ORE_RUPLE  = Ruple(1, 0, 0, 0)

    def __init__(self, blueprint, terminal_minute):
        self.ORACLE_TERMINAL_MINUTE = terminal_minute

        self.__robot_deltas = {
            ACTION_ORE:      self.ORE_RUPLE,
            ACTION_CLAY:     Ruple(0, 1, 0, 0),
            ACTION_OBSIDIAN: Ruple(0, 0, 1, 0),
            ACTION_GEODE:    Ruple(0, 0, 0, 1),
            }

        self.__cost_deltas = {
            ACTION_ORE:      Ruple(blueprint.ore_cost, 0, 0, 0),
            ACTION_CLAY:     Ruple(blueprint.clay_cost,0, 0, 0),
            ACTION_OBSIDIAN: Ruple(blueprint.obsidian_cost[0], blueprint.obsidian_cost[1], 0, 0),
            ACTION_GEODE:    Ruple(blueprint.obsidian_cost[0], 0, blueprint.obsidian_cost[1], 0),
            }

        self.__active = [Fact(Genome([]), 0, self.ORE_RUPLE, self.ZERO_RUPLE, self.ORE_RUPLE)]
        self.__best   = 0

    def oracle_grow(self):
        new_active = []
        for fact in self.__active:
            if fact.FACT_MINUTE > self.ORACLE_TERMINAL_MINUTE: continue
            if self.__best <  fact.FACT_RESOURCE_TOTAL_RUPLE.RUPLE_GEODE:
                self.__best = fact.FACT_RESOURCE_TOTAL_RUPLE.RUPLE_GEODE
                log(f"A new best is -> {fact}")
            for action in self.ALL_ACTIONS:
                new_genome        = fact.FACT_GENOME.genome_factory(action)
                delta_robot_ruple = self.__robot_deltas[action]
                next_cost_ruple   = self.__cost_deltas[action]

                # log(f"{new_genome}  {delta_robot_ruple}  {next_cost_ruple}")
                # log(f"  starting with -> {fact}")

                next_fact         = fact.fact_feed_forward(new_genome,
                                                           next_cost_ruple,
                                                           delta_robot_ruple)
                if next_fact is None: continue
                new_active.append(next_fact)
        self.__active = new_active
        return len(self.__active), self.__best


if __name__ == '__main__':
    if True:
        data = parse_data(sample_input.split('\n'))
    else:
        data = parse_data(open(DATAFILE, 'r'))

    log(f"Its on...")

    for blueprint in [data[0]]:
        oracle = Oracle(blueprint, 24)
        loops = 0
        while True:
            active_count, best_so_far = oracle.oracle_grow()
            loops += 1
            log(f"{loops=}: {best_so_far=} and {active_count=}")

    log(f"Its over")


