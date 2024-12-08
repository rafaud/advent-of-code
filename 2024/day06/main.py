import copy
from math import floor
from time import sleep, time

import input_reader
import numpy as np

from model.FacilityMap import FacilityMap

# DEBUG = True
DEBUG = False

input_data = input_reader.ged_data(DEBUG)
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

time_stop = time()
print(f"Loop count: {loop_count}")

run_time = time_stop - time_start
time_min = int(floor(run_time/60))
time_s = int(floor(run_time - time_min*60))
time_ms = int(floor((run_time - time_min*60 - time_s) * 1000))

print(f"Run time: {time_min}min {time_s}s {time_ms}ms")
with open("output.txt", "w") as file:
    file.write(str(facility_map))

