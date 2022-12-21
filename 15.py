import logging

DATAFILE = "./data/15.txt"

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(message)s')
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
    def __init__(self, sensor_line_definition):
        log.debug(f"PARTIAL: sensor_line_definition -> {sensor_line_definition}")
        xe_split = sensor_line_definition.split("x=")
        ye_split = sensor_line_definition.split("y=")
        log.debug(f"PARTIAL: xe_split -> {xe_split}")
        log.debug(f"PARTIAL: ye_split -> {ye_split}")
        self.SENSOR_MY_X     = int(xe_split[1].split(",")[0])
        self.SENSOR_MY_Y     = int(ye_split[1].split(":")[0])
        self.SENSOR_BEACON_X = int(xe_split[2].split(",")[0])
        self.SENSOR_BEACON_Y = int(ye_split[2])

    def __str__(self):
        return            f"Sensor at x={self.SENSOR_MY_X    }, y={self.SENSOR_MY_Y    }: " +\
               f"closest beacon is at x={self.SENSOR_BEACON_X}, y={self.SENSOR_BEACON_Y}"

def parse_input(input_string):
    return [Sensor(line) for line in input_string.strip().split("\n")]

if __name__ == '__main__':
    if False:
        sensor_list = parse_input(sample_data)
    else:
        sensor_list = parse_input(open(DATAFILE, 'r').read())

    log.info("Reflecting input...")
    for sensor in sensor_list:
        log.debug(str(sensor))




