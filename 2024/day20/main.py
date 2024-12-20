import copy
import heapq
from collections import defaultdict

import numpy as np

# with open("input_test.txt") as f:
with open("input.txt") as f:
    data = f.read()

map_array = np.array([list(line) for line in data.split("\n")])

start = 0,0
end = 0,0
for row, line in enumerate(map_array):
    for col, char in enumerate(line):
        if char == "S":
            start = (row, col)
            map_array[row, col] = "."
        if char == "E":
            end = (row, col)
            map_array[row, col] = "."

def find_path(_plan: np.ndarray, _start: (int, int), _end: (int, int)):
    # Declare directions, for finding adjacent tiles
    _directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    # Get map size
    _h, _w = _plan.shape

    # Create heap queue with tiles to be checked
    _queue = [(0, _start)]

    # Create dictionary with best distance for each tile
    _distances = {_start: 0}

    # Create dictionary with tiles and best previous tile
    _predecessors = {}

    # While there are tile in queue, check tile with shorted distance from start (so first one in heap queue)
    while _queue:
        # Get first tile
        _cost, _current_position = heapq.heappop(_queue)
        _y, _x = _current_position
        # Check if first tile is the end tile, if so the end was found and we can return found path
        if _current_position == _end:
            # Path found, return it
            _path = []
            # Start going backwards
            while _current_position is not None:
                # Append tile
                _path.append(_current_position)
                # Get previous tile (we only save the best ones)
                _current_position = _predecessors.get(_current_position, None)
            # Return cost and reconstructed path (in reverse)
            return _cost, _path[::-1], _distances

        # Check each possible move direction
        for _dy, _dx in _directions:
            # Find position of next tile
            _ny, _nx = _y + _dy, _x + _dx

            # Check if tile is valid tile to move on
            if 0 <= _ny < _h and 0 <= _nx < _w and _plan[_ny, _nx] == ".":
                # We took one step so new step count it increased by one
                _new_cost = _cost + 1
                _neighbour = (_ny, _nx)
                # If this is first time we visit this tile (_neighbour not in _distances),
                # or we found shorter distance to tile.
                if _neighbour not in _distances or _new_cost < _distances[_neighbour]:
                    # Save new closer distance as best distance
                    _distances[_neighbour] = _new_cost

                    # Save current tile as best predecessor of this new tile
                    _predecessors[_neighbour] = _current_position

                    # Put this tile in queue for further checking
                    heapq.heappush(_queue, (_new_cost, _neighbour))

normal_path = find_path(map_array, start, end)

def get_cheat_distance(a: (int, int), b: (int, int)):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

saved_times = defaultdict(int)
possible_cheats = {}
max_cheat_distance = 20
min_time_saved = 100
for i, possible_start in enumerate(normal_path[1]):
    print("Checking cheat", i, "of", len(normal_path[1]), "possible cheats...")
    for possible_end in normal_path[1]:
        # Check if we're not checking the same tile
        if possible_start == possible_end: continue

        # Check if tiles are not next to each other (it would mean normal path)
        if get_cheat_distance(possible_start, possible_end) == 1: continue

        # Check if it's possible to get to end tile in maximum cheat distance
        if get_cheat_distance(possible_start, possible_end) > max_cheat_distance: continue

        # Check if cheat is actually saving time
        time_saved = normal_path[2][possible_end] - normal_path[2][possible_start] - get_cheat_distance(possible_start, possible_end)
        if time_saved <= 0: continue
        # And if it save minimum of required saved time
        if time_saved < min_time_saved: continue
        saved_times[time_saved] += 1
        possible_cheats[(possible_start, possible_end)] = time_saved

answer = 0
print(f"Normal path cost: {normal_path[0]}")
for key in sorted(saved_times.keys()):
    answer += saved_times[key]
    print(f"There are {saved_times[key]} cheats that save {key} steps.")

print(f"Answer: {answer}")
print(f"Max distance", normal_path[0])