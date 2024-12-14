import copy
from collections import defaultdict
import aoc_helper
from typing import Tuple
import numpy as np

# DEBUG = True
DEBUG = False

t_map = np.array([[int(value) for value in data.strip()] for data in aoc_helper.get_data(DEBUG)])
print(t_map)

def clamp_location(_location):
    loc_y = _location[0]
    loc_x = _location[1]

    min_y = 0
    min_x = 0

    max_y = t_map.shape[0]
    max_x = t_map.shape[1]

    return max(min(loc_y, max_y), min_y), max(min(loc_x, max_x), min_x)

def get_height_for(_location: Tuple[int, int]):
    _location = clamp_location(_location)
    try:
        height = t_map[_location[0]][_location[1]]
        return height
    except IndexError:
        return -1
    except Exception as e:
        print(e)
        return -1

def get_next_step(_location: Tuple[int, int]):
    steps = []
    _location = clamp_location(_location)
    height = get_height_for(_location)
    if height + 1 == get_height_for((_location[0] + 1, _location[1])):
        steps.append((_location[0] + 1, _location[1]))
    if height + 1 == get_height_for((_location[0] - 1, _location[1])):
        steps.append((_location[0] - 1, _location[1]))
    if height + 1 == get_height_for((_location[0], _location[1] - 1)):
        steps.append((_location[0], _location[1] - 1))
    if height + 1 == get_height_for((_location[0], _location[1] + 1)):
        steps.append((_location[0], _location[1] + 1))
    return steps

start_locations = []

for i in range(t_map.shape[0]):
    for j in range(t_map.shape[1]):
        if int(get_height_for((i, j))) == 0:
            start_locations.append((i, j))

print(f"Start locations: {start_locations}")

paths = [[start_location] for start_location in start_locations]

def expand_paths(_paths):
    _expanded_paths = []
    for path in _paths:
        last_step = path[-1]
        next_steps = get_next_step(last_step)
        if next_steps:
            for next_step in next_steps:
                new_path = copy.deepcopy(path)
                new_path.append(next_step)
                _expanded_paths.append(new_path)
                _expanded_paths = expand_paths(_expanded_paths)
        else:
            _expanded_paths.append(path)
    return _expanded_paths

expanded_paths = expand_paths(paths)
final_paths = defaultdict(list)
for expanded_path in expanded_paths:
    if len(expanded_path) == 10:
        final_paths[expanded_path[0]].append(expanded_path[-1])

unique_destinations = defaultdict(set)
for key, value in final_paths.items():
    unique_destinations[key] = set(value)


total = 0
for key, value in unique_destinations.items():
    total += len(value)
print(f"Total, unique destinations: {total}")

total = 0
for key, value in final_paths.items():
    total += len(value)
print(f"Total unique paths: {total}")

