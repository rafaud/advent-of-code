from enum import Enum
from unittest import case

import numpy as np
import input_reader

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def get_rotated_right(self):
        match self:
            case Direction.UP:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.LEFT
            case Direction.LEFT:
                return Direction.UP

    def is_horizontal(self):
        return self == Direction.LEFT or self == Direction.RIGHT

    def is_vertical(self):
        return self == Direction.DOWN or self == Direction.UP

class Position:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

class Guard:
    def __init__(self, pos: Position, direction: Direction):
        self.pos = pos
        self.direction = direction

    def turn_right(self):
        self.direction = self.direction.get_rotated_right()

class Tile:
    def __init__(self,
                 is_start: bool = False,
                 is_obstacle: bool = False,
                 direction: [Direction] = None,
                 is_loop_obstacle: bool = False,
                 is_turn_right: bool = False,
                 is_passed: bool = False
                 ):
        if direction is None:
            self.direction = []
        self.is_start = is_start
        self.is_obstacle = is_obstacle
        self.is_loop_obstacle = is_loop_obstacle
        self.is_turn_right = is_turn_right
        self.is_passed = is_passed

    @property
    def is_vertical(self):
        return  Direction.UP in self.direction or Direction.DOWN in self.direction

    @property
    def is_horizontal(self):
        return Direction.LEFT in self.direction or Direction.RIGHT in self.direction

    @property
    def is_horizontal_and_vertical(self):
        return self.is_vertical and self.is_horizontal

    def __str__(self):
        if self.is_start:
            return "▲"
        if self.is_obstacle:
            return "▓"
        if self.is_loop_obstacle:
            return "○"
        if self.is_horizontal_and_vertical:
            return "╬"
        elif self.is_turn_right:
            if self.direction[0] == Direction.UP:
                return "╔"
            elif self.direction[0] == Direction.RIGHT:
                return "╗"
            elif self.direction[0] == Direction.DOWN:
                return "╝"
            elif self.direction[0] == Direction.LEFT:
                return "╚"
        elif self.is_horizontal:
            return "═"
        elif self.is_vertical:
            return "║"
        else:
            return "░"

    def __repr__(self):
        return self.__str__()

DEBUG = True
# DEBUG = False

input_data = input_reader.ged_data(DEBUG)
input_data = np.array([[value for value in line.strip()] for line in input_data])

guard = Guard(Position(0, 0), Direction.UP)
tile_map = [[Tile() for _ in row] for row in input_data]

# Find starting position
for y in range(input_data.shape[0]):
    for x in range(input_data[y].shape[0]):
        if input_data[y, x] == "^":
            # 0 - up, 1
            guard.direction = Direction.UP
            guard.pos = Position(x, y)
            input_data[y, x] = "x"
            tile_map[y][x].is_start = True
            tile_map[y][x].direction.append(guard.direction)
        if input_data[y, x] == "#":
            tile_map[y][x].is_obstacle = True


def get_next_tile():
    if guard.direction == Direction.UP:
        # check tile y-1
        if guard.pos.y == 0: return "*"
        return guard.pos.y - 1, guard.pos.x
    elif guard.direction == Direction.DOWN:
        # check tile y + 1
        if guard.pos.y == input_data.shape[0] - 1: return "*"
        return guard.pos.y + 1, guard.pos.x
    elif guard.direction == Direction.LEFT:
        # check tile x - 1
        if guard.pos.x == 0: return "*"
        return guard.pos.y, guard.pos.x - 1
    elif guard.direction == Direction.RIGHT:
        # check tile x + 1
        if guard.pos.x == input_data.shape[1] - 1: return "*"
        return guard.pos.y, guard.pos.x + 1

def move_guard():
    if guard.direction == Direction.UP:
        guard.pos.y -= 1
    elif guard.direction == Direction.DOWN:
        guard.pos.y += 1
    elif guard.direction == Direction.LEFT:
        guard.pos.x -= 1
    elif guard.direction == Direction.RIGHT:
        guard.pos.x += 1


guard_moving = True
safety = 9999999
while guard_moving:
    if safety > 0:
        safety -= 1
    else:
        guard_moving = False

    next_tile = get_next_tile()
    if next_tile == "*":
        guard_moving = False
        break

    next_tile_value = input_data[next_tile[0], next_tile[1]]
    if next_tile_value == "." or next_tile_value == "x":
        if tile_map[guard.pos.y][guard.pos.x].is_passed:
            if tile_map[guard.pos.y][guard.pos.x].direction[0] == guard.direction.get_rotated_right():
                tile_map[next_tile[0]][next_tile[1]].is_loop_obstacle = True
        move_guard()
        input_data[guard.pos.y, guard.pos.x] = "x"
        tile_map[guard.pos.y][guard.pos.x].is_passed = True
        tile_map[guard.pos.y][guard.pos.x].direction.append(guard.direction)

    elif next_tile_value == "#":
        guard.turn_right()
        tile_map[guard.pos.y][guard.pos.x].is_turn_right = True
    print("\n".join(["".join([str(tile) for tile in line]) for line in tile_map]))
    print(tile_map[guard.pos.y][guard.pos.x].direction[0])
    print("\n\n")

# [print("".join(line)) for line in input_data]

total = sum([1 for row in input_data for value in row if value == "x"])
print(f"Total 'x' after calculating guard path: {total}")


lines = ["".join([str(tile) for tile in line]) for line in tile_map]
with open("../output.txt", "w") as file:
    file.write("\n".join(lines))