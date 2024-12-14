import copy
from math import floor
from time import sleep, time

import aoc_helper
import numpy as np

from model.FacilityMap import FacilityMap

# DEBUG = True
DEBUG = False

input_data = aoc_helper.get_data(DEBUG)
input_data = np.array([[value for value in line.strip()] for line in input_data])

empty_facility_map = FacilityMap.from_string_array(input_data)
facility_map = copy.deepcopy(empty_facility_map)

guard_move = True
while guard_move is not None:
    guard_move = facility_map.move_guard()
    if not guard_move:

        break
    None

passed_tiles = sum([1 for row in facility_map.tiles for tile in row if tile.is_passed])
print(f"Passed tiles: {passed_tiles}")
time_start = time()
loop_count = 0
for i in range(facility_map.tiles.shape[0]):
    for j in range(facility_map.tiles.shape[1]):
        # print(f"Test tile: y:{i}, x:{j}")
        if facility_map.tiles[i, j].is_passed:
            print(f"Checking tile: x: {j}, y: {i}")
            facility_map_copy = copy.deepcopy(empty_facility_map)
            facility_map_copy.tiles[i, j].is_loop_obstacle = True
            guard_move = True
            while guard_move is not None:
                if not guard_move:
                    loop_count += 1
                    print(f"Loop found! \nCount: {loop_count}")
                    facility_map.tiles[i, j].is_loop_obstacle = True
                    break
                guard_move = facility_map_copy.move_guard()

print(f"Loop count: {loop_count}")

time_stop = time()
run_time = time_stop - time_start
print(aoc_helper.format_time(run_time))
with open("output.txt", "w") as file:
    file.write(str(facility_map))

