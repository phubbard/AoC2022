"""
Transcription of code cells from Jupyter notebook for Advent of Code 2022 problem 15.
Notebook date was December 22, 2022.

Date:  December 24, 2022

Note:  To run this in ipython,

In [1]: exec(open('15.py').read())

in the same directory as the datafile 15.txt
"""

###
#  Cell 1
###

import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(linewidth=250)

###
#  Cell 2
###

with open("data/15.txt") as f:
    contents = f.readlines()


###
#  Cell 3
###

def parse_line(l):
    """
    Parse a line from the data file and return two ordered pairs, sensor and beacon
    """
    a = l.rstrip().split(' ')
    sx = int(a[2].split('=')[1].rstrip(','))
    sy = int(a[3].split('=')[1].rstrip(':'))
    bx = int(a[-2].split('=')[1].rstrip(','))
    by = int(a[-1].split('=')[1])
    return [sx, sy], [bx, by]


def interval_contraction(ilist):
    slist = [x for x in ilist]
    slist.sort(key=lambda x: x[0])
    if len(slist) > 0:
        rlist = [slist[0]]
        for i in slist:
            comp = rlist[-1]
            if i[0] <= comp[
                1] + 1:  # This is because [[1,2],[3,4]] should become [1,4] since we are only considering integers
                new = [comp[0], max(comp[1], i[1])]
                rlist[-1] = new
                # print("Previous: {}, Next: {}, New: {}, resulting list: {}".format(comp,i,new,rlist))
            else:
                rlist.append(i)
                # print(comp,i,rlist)
    else:
        rlist = []
    return rlist


###
#  Cell 4
###

MINY = 3000000
MAXY = 4000000

coverage = {}

for line in contents:
    s, b = parse_line(line)
    md = np.abs(np.array(s) - np.array(b)).sum()
    sy = s[1]
    sx = s[0]
    print("Sensor y coordinate: {}, Manhattan distance: {},  min y sensed: {}, max y sensed: {}".format(sy, md, sy - md,
                                                                                                        sy + md))
    print(line)

    for dy in range(-md, md + 1):
        yval = sy + dy
        if (yval >= MINY) and (yval <= MAXY):
            dx = md - np.abs(dy)
            new = [sx - dx, sx + dx]
            if yval in coverage:
                new_list = coverage[yval] + [new]
                # print(new_list)
                coverage[yval] = interval_contraction(new_list)
            else:
                coverage[yval] = [new]
            # print("y coordinate: {}, list: {}".format(yval,coverage[yval]))

###
#  Cell 5
###

for k in coverage:
    if len(coverage[k]) > 1:
        print("Possible y value: {}".format(k))

###
#  Cell 6
###

# This is the yvalue you should see from above
print(coverage[3211051])

###
#  Cell 7
###
# And this is computed using the results from the previous two lines to get the submission number.
submit_number = (2960218 + 1) * (4000000) + 3211051
print(submit_number)

