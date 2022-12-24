import logging
import multiprocessing
import sys

DATAFILE = "./data/15.txt"

logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
log = logging.getLogger()


sample_data = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""

sample_ans_y10 = 26


class Sensor:
    __slots__ = "SENSOR_MY_X", "SENSOR_MY_Y", "SENSOR_BEACON_X", "SENSOR_BEACON_Y", "SENSOR_MANHATTAN_X", "SENSOR_MANHATTAN_Y", "SENSOR_MANHATTAN_DISTANCE",

    def __init__(self, sensor_line_definition):
        log.debug(f"PARTIAL: sensor_line_definition -> {sensor_line_definition}")
        xe_split = sensor_line_definition.split("x=")
        ye_split = sensor_line_definition.split("y=")
        log.debug(f"PARTIAL: xe_split -> {xe_split}")
        log.debug(f"PARTIAL: ye_split -> {ye_split}")
        self.SENSOR_MY_X               = int(xe_split[1].split(",")[0])
        self.SENSOR_MY_Y               = int(ye_split[1].split(":")[0])
        self.SENSOR_BEACON_X           = int(xe_split[2].split(",")[0])
        self.SENSOR_BEACON_Y           = int(ye_split[2])
        self.SENSOR_MANHATTAN_X        = abs(self.SENSOR_BEACON_X - self.SENSOR_MY_X)
        self.SENSOR_MANHATTAN_Y        = abs(self.SENSOR_BEACON_Y - self.SENSOR_MY_Y)
        self.SENSOR_MANHATTAN_DISTANCE = self.SENSOR_MANHATTAN_X + self.SENSOR_MANHATTAN_Y

    def __str__(self):
        return            f"Sensor at x={self.SENSOR_MY_X    }, y={self.SENSOR_MY_Y    }: " +\
               f"closest beacon is at x={self.SENSOR_BEACON_X}, y={self.SENSOR_BEACON_Y}; " +\
               f"distance={self.SENSOR_MANHATTAN_DISTANCE}"

    def is_point_in_manhattan_range(self, test_x, test_y):
        delta_x = abs(self.SENSOR_MY_X - test_x)
        delta_y = abs(self.SENSOR_MY_Y - test_y)
        manhattan = delta_x + delta_y
        return manhattan <= self.SENSOR_MANHATTAN_DISTANCE


def parse_input(input_string):
    return [Sensor(line) for line in input_string.strip().split("\n")]


def manhattan_distance(one, two):
    x_dist = abs(one[0] - two[0])
    y_dist = abs(one[1] - two[1])
    return x_dist + y_dist


def all_positions(input_sensor: Sensor, y_val):
    sensor = (input_sensor.SENSOR_MY_X, input_sensor.SENSOR_MY_Y)
    beacon = (input_sensor.SENSOR_BEACON_X, input_sensor.SENSOR_BEACON_Y)
    distance = manhattan_distance(sensor, beacon)
    # For a sensor at x,y and within the manhattan distance, return a
    # vector of x that have the given y_val.
    # Feels like rasterizing at a given scan line.
    delta_y = abs(sensor[1] - y_val)
    length = distance - delta_y
    if length <= 0:
        # Triangle does not intersect the y_val line
        return []
    rc = list(range(sensor[0] - length, sensor[0] + length + 1))
    # Remove any beacons in the line
    # if beacon[1] == y_val:
    #     rc.remove(beacon[0])
    return rc


def run_chris_algo(data):
    # Part one solver
    scan_line = set()
    Y_VAL = 2000000
    for sensor in data:
        log.debug(f"checking sensor {sensor}")
        # Merge lists and drop duplicates
        scan_line = scan_line.union(all_positions(sensor, Y_VAL))
    log.info(f"Done with sensors, {len(scan_line)} found")


def return_missing(scanline, max_value):
    for idx, value in enumerate(scanline):
        if idx != value:
            return idx
    return None


def part_two_process_line(inp_data, row_index):
    # Expects a single row to search. If we find our spot, log.warn it out, otherwise exit silently.
    if row_index % 10 == 0:
        log.info(f"Row {row_index} running")
    search_extent = 4000000
    scan_line = set()
    for sensor in inp_data:
        scan_line = scan_line.union(all_positions(sensor, row_index))

    data = list(scan_line)
    data.sort()
    clipped_set = set(data).intersection(range(0, search_extent + 1))
    log.debug(f"Done with sensors, {len(clipped_set)} positions found")
    if len(clipped_set) != (search_extent + 1):
        x = return_missing(clipped_set, search_extent)
        if not x:
            return
        freq = x * 4000000 + row_index
        log.warning(f"Found empty spot at {len(clipped_set)} ({x}, {row_index}) => {freq}")
        sys.exit(0)


def run_part_two(input_data):
    search_extent = 4000000
    log.info("Starting pool")
    pool = multiprocessing.Pool()
    pool.starmap(part_two_process_line, [(input_data, x) for x in range(search_extent)])
    log.info('Done!')


if __name__ == '__main__':
    input_data = parse_input(open(DATAFILE, 'r').read())
    # input_data = parse_input(sample_data)
    # run_chris_algo(data)
    run_part_two(input_data)

    # frequency_x_scalar = 4000000
    #
    # if False:
    #     sensor_list = parse_input(sample_data)
    #     test_y_index = 10
    #     search_extent = 20
    #     expected_answer = 56000011
    #     c_file_name = "massaged_sensor_15.c"
    # else:
    #     sensor_list = parse_input(open(DATAFILE, 'r').read())
    #     test_y_index = 2000000
    #     search_extent = 4000000
    #     expected_answer = -1
    #     c_file_name = "massaged_sensor_15_final.c"
    #
    # log.info("Reflecting input...")
    # for sensor in sensor_list:
    #     log.debug(str(sensor))
    #
    # log.info("Determine APPROXIMATE extents...")
    # min_x = sensor_list[0].SENSOR_MY_X
    # max_x = min_x
    # min_y = sensor_list[0].SENSOR_MY_Y
    # max_y = min_y
    # for sensor in sensor_list:
    #     min_x = min(min_x, sensor.SENSOR_MY_X, sensor.SENSOR_BEACON_X)
    #     min_y = min(min_y, sensor.SENSOR_MY_Y, sensor.SENSOR_BEACON_Y)
    #     max_x = max(max_x, sensor.SENSOR_MY_X, sensor.SENSOR_BEACON_X)
    #     max_y = max(max_y, sensor.SENSOR_MY_Y, sensor.SENSOR_BEACON_Y)
    # approx_extent_x = max_x - min_x
    # approx_extent_y = max_y - min_y
    # log.info(f" -> min_x:{min_x} max_y:{max_y}  -> approx_extent_x:{approx_extent_x}")
    # log.info(f" -> min_x:{min_x} max_y:{max_y}  -> approx_extent_y:{approx_extent_y}")
    #
    # megabytes_approx = (approx_extent_x * approx_extent_y * 4) / 1000000
    # log.info(f"NAive full grid storage requirements: {megabytes_approx} megabytes (!!!)")
    #
    # log.info(f"Given distance, determine max covered spots...")
    # min_covered_x = sensor_list[0].SENSOR_MY_X
    # max_covered_x = sensor_list[0].SENSOR_MY_X
    # for sensor in sensor_list:
    #     min_covered_x = min(min_covered_x, sensor.SENSOR_MY_X - sensor.SENSOR_MANHATTAN_DISTANCE)
    #     max_covered_x = max(max_covered_x, sensor.SENSOR_MY_X + sensor.SENSOR_MANHATTAN_DISTANCE)
    #
    # log.info(f"  --> max covered  min_covered_x:{min_covered_x} max_covered_x:{max_covered_x}")
    #
    # part_one = False
    # if part_one:
    #     too_big_to_fail = 7000000  # Result here is 5394423 -> correct
    #     log.info(f"locate along test_y_index:{test_y_index} ...")
    #     covered_count = 0
    #     for x in range(-too_big_to_fail, too_big_to_fail):
    #         if 0 == (x % 1000000): log.debug(f"at x = {x}")
    #         is_covered = False
    #         is_beacon  = False
    #         is_sensor  = False
    #         for sensor in sensor_list:
    #             is_covered = is_covered or sensor.is_point_in_manhattan_range(x, test_y_index)
    #             is_beacon  = is_beacon or ((x == sensor.SENSOR_BEACON_X) and (test_y_index == sensor.SENSOR_BEACON_Y))
    #             is_sensor  = is_sensor or ((x == sensor.SENSOR_MY_X) and (test_y_index     == sensor.SENSOR_MY_Y))
    #         if is_covered and not is_beacon and not is_sensor:
    #             covered_count += 1
    #     log.info(f"    ... yields covered_count:{covered_count}")
    #
    # if True:
    #     log.info(f"Generate C to do it...")
    #     cpp = []
    #     cpp          += ["const struct sensor_t sensors[] = {"]
    # too_big_to_fail = 8000000  # Yiedled 4991702, failed with "too low"
    # log.info(f"locate along test_y_index:{test_y_index} ...")
    # covered_count = 0
    # for x in range(-too_big_to_fail, too_big_to_fail):
    #     if 0 == (x % 1000000): log.debug(f"at x = {x}")
    #     is_covered = False
    #     is_beacon  = False
    #     is_sensor  = False
    #     for sensor in sensor_list:
    #         cpp +=      ["    {" + f".location_x={sensor.SENSOR_MY_X}, .location_y={sensor.SENSOR_MY_Y}, .distance={sensor.SENSOR_MANHATTAN_DISTANCE}" + "},", ]
    #     cpp          += ["};"]
    #     cpp          += [""]
    #     cpp          += [f"const int search_extent = {search_extent};"]
    #     cpp          += [""]
    #     cpp          += [f"const int expected_answer = {expected_answer};"]
    #     cpp          += [""]
    #     cpp          += [f"const int frequency_x_scalar = {frequency_x_scalar};"]
    #     with open(c_file_name, 'w') as file:
    #         file.write("\n".join(cpp))
