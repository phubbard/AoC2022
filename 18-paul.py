
# Working from https://medium.com/@alexeyyurasov/3d-modeling-with-python-c21296756db2
# f-string tricks from https://towardsdatascience.com/python-f-strings-are-more-powerful-than-you-might-think-8271d3efbd7d

import logging
import numpy as np
from scipy import spatial
from tqdm import tqdm

# The Brad-config
logging.basicConfig(level=logging.DEBUG, format='%(pathname)s(%(lineno)s): %(levelname)s %(message)s')
log = logging.getLogger()

sample_data = """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""

sample_answer = 64


def parse_data(data_lines):
    rc = []
    for line in tqdm(data_lines):
        parsed = line.strip().split(',')
        if len(parsed) != 3:
            log.warning(f"Skipped line '{line}'")
            continue
        rc.append([parsed[0], parsed[1], parsed[2]])
    return np.array(rc)


def orchestrate():
    vertices = parse_data(sample_data.split('\n'))
    hull = spatial.ConvexHull(vertices)
    log.info(f"Hull {hull.area = } {hull.volume = }")
    # faces = hull.simplices


if __name__ == '__main__':
    orchestrate()