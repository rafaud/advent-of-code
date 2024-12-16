import math
from time import sleep

import numpy as np

input_file = "input.txt"

with open(input_file) as f:
    maze = np.array([[ch for ch in line.strip()] for line in f.readlines()])

start = ()
stop = ()

for row, line in enumerate(maze):
    for col, ch in enumerate(line):
        if ch == "S":
            start = (row, col)
            maze[row, col] = "."
        if ch == "E":
            stop = (row, col)
            maze[row, col] = "."

#        0
#        up
#    3       1
#   left    right
#        2
#       down


direction = 1
rotation_cost = 1000
step_cost = 1

maze_graph = {}

def get_neighbours(pos: (int, int), of_type: str = ".") -> [(int, int)]:
    moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    return_tiles = []
    for move in moves:
        next_tile = tuple([sum(foo) for foo in zip(move, pos)])
        if maze[*next_tile] == of_type:
            return_tiles.append(next_tile)
        else:
            return_tiles.append((0, 0))
    return return_tiles


cost_map = np.full(maze.shape, fill_value=-1, dtype=int)
previous_map = [[[] for _ in range(maze.shape[1])] for _ in range(maze.shape[0])]
path = []
cost_map[start] = 0

visited = set()
current_tiles = [(start, 1)]

def update_path_for_position(pos: (int, int), _direction: int) -> [(int, int)]:
    updated_tiles = []
    for i, neighbour in enumerate(get_neighbours(pos)):
        if neighbour == (0, 0): continue
        current_cost = cost_map[*pos]
        if cost_map[neighbour] == -1:
            turns = abs(_direction - i)
            if turns == 3: turns = 1
            cost_map[neighbour] = current_cost + step_cost + turns * rotation_cost
            updated_tiles.append((neighbour, i))
            previous_map[neighbour[0]][neighbour[1]].append(pos)
    return updated_tiles

def get_path_string() -> str:
    return_string = ""
    for line in path_map:
        for value in line:
            return_string += value
        return_string += "\n"
    return return_string


while cost_map[stop] == -1:
    current_tiles.sort(key=lambda x: cost_map[x[0]])
    first_tile = current_tiles[0]
    path.append(first_tile)
    path = path[:path.index(first_tile)]
    path.append(first_tile)
    new_tiles = update_path_for_position(*first_tile)
    current_tiles = current_tiles[1:]
    current_tiles += new_tiles

path_map = np.full(maze.shape, fill_value=" ", dtype=str)

def get_past(pos):
    y, x = pos
    return previous_map[y][x]

def update_path_map(pos):
    # sleep(0.1)
    pos_y, pos_x = pos
    for previous in previous_map[pos_y][pos_x]:
        prev_y, prev_x = previous
        path_map[prev_y][prev_x] = "O"
        if previous != start:
            update_path_map(previous)

    for neighbour in get_neighbours(pos):
        n_y, n_x = neighbour
        if neighbour in previous_map[pos_y][pos_x]: continue
        if cost_map[n_y][n_x] == -1: continue
        if path_map[n_y][n_x] == "O": continue
        if pos in get_past(neighbour): continue
        print(pos, neighbour, previous_map[pos_y][pos_x], cost_map[n_y][n_x])
        update_path_map(neighbour)
    path_map[pos_y][pos_x] = "X"
    # print(path_map)
    path_map[pos_y][pos_x] = "O"



update_path_map(stop)
path_map[start[0]][start[1]] = "S"
path_map[stop[0]][stop[1]] = "E"
print(get_path_string())
print(sum([1 for row in path_map for value in row if value == "O"]))
