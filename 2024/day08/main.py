import math
from math import floor

import numpy as np

import aoc_helper
from collections import defaultdict

# DEBUG = True
DEBUG = False

input_data = np.array([[value for value in data.strip()] for data in aoc_helper.ged_data(DEBUG)])

antennas = defaultdict(list)

for i, line in enumerate(input_data):
    for j, value in enumerate(line):
        if value != ".":
            antennas[value].append((i, j))

def get_pairs(l: list) -> list:
    _pairs = []
    for first_index in range(len(l)):
        for second_index in range(first_index + 1, len(l)):
            _pairs.append((l[first_index], l[second_index]))
    return _pairs

tmp = {}
for antenna, coords in antennas.items():
    pairs = get_pairs(coords)
    tmp[antenna] = {"coords": coords, "pairs": pairs}

antennas = tmp
print(antennas)

