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

def get_distance_for_pair(_pair):
    return _pair[0][0] - _pair[1][0], _pair[0][1] - _pair[1][1]

def get_anti_node_for_distance(_antenna, _distance, mul=1, subtract=False):
    if subtract:
        _distance = (-_distance[0], -_distance[1])
    _anti_node = (_antenna[0] + _distance[0] * mul, _antenna[1] + _distance[1] * mul)
    if check_bounds(_anti_node):
        return _anti_node
    else:
        return None

def get_possible_anti_nodes_for_pair(_pair, _resonant = False):
    _return_nodes = ()
    distance = get_distance_for_pair(_pair)
    if _resonant:
        _return_nodes += _pair
        multiplier = 1
        while _anti_node := get_anti_node_for_distance(pair[0], distance, mul=multiplier):
            _return_nodes += (_anti_node,)
            multiplier += 1

        multiplier = 1
        while _anti_node := get_anti_node_for_distance(pair[1], distance, mul=multiplier, subtract=True):
            _return_nodes += (_anti_node,)
            multiplier += 1
    else:
        # first_anti_node
        if _anti_node := get_anti_node_for_distance(_pair[0], distance):
            _return_nodes += (_anti_node,)
        # second_anti_node
        if _anti_node := get_anti_node_for_distance(_pair[1], distance, subtract=True):
            _return_nodes += (_anti_node,)
    return _return_nodes


def check_bounds(_coords, size=input_data.shape[0]):
    return 0 <= _coords[0] < size and 0 <= _coords[1] < size

tmp = {}
for antenna, coords in antennas.items():
    pairs = get_pairs(coords)
    tmp[antenna] = {"coords": coords, "pairs": pairs}

antennas = tmp

anti_nodes_set = set()
for antenna, data in antennas.items():
    anti_nodes = []
    for pair in data["pairs"]:
        anti_nodes += get_possible_anti_nodes_for_pair(pair)
    antennas[antenna]["anti_nodes"] = anti_nodes
    anti_nodes_set.update(anti_nodes)

print(f"There are {len(anti_nodes_set)} anti-nodes, without resonant frequencies.")

anti_nodes_set = set()
for antenna, data in antennas.items():
    anti_nodes = []
    for pair in data["pairs"]:
        anti_nodes += get_possible_anti_nodes_for_pair(pair, True)
    antennas[antenna]["anti_nodes"] = set(anti_nodes)
    anti_nodes_set.update(anti_nodes)

print(f"There are {len(anti_nodes_set)} anti-nodes, with resonant frequencies.")

for antenna, data in antennas.items():
    for anti_node in data["anti_nodes"]:
        if input_data[anti_node[0]][anti_node[1]] == ".":
            input_data[anti_node[0]][anti_node[1]] = "#"

with open("output.txt", "w") as f:
    f.write("\n".join(["".join(line) for line in input_data]))


