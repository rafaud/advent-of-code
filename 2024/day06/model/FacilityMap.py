import numpy as np

from .Tile import Tile
from .Guard import Guard
from .Direction import Direction
from .Position import Position

class FacilityMap:
    def __init__(self, size):
        # Initialize empty tile map with given size
        self.tiles = np.array([[Tile() for _ in range(size[1])] for _ in range(size[0])])
        self._starting_tile = None
        self._guard = None
        self.edge_case = 0

    @classmethod
    def from_string_array(cls, array: np.ndarray):
        instance = FacilityMap(array.shape)
        for y in range(array.shape[0]):
            for x in range(array.shape[1]):
                if array[y, x] == "#":
                    instance.get_tile_xy(x, y).is_obstacle = True
                if array[y, x] == "^":
                    instance.get_tile_xy(x, y).is_starting_position = True
                    instance.get_tile_xy(x, y).pass_directions.append(Direction.UP)
                    instance._starting_tile = Position(x, y)
                    instance._guard = Guard(pos=instance._starting_tile,
                                            direction=Direction.UP)
        return instance

    def get_tile_tuple(self, tup) -> Tile:
        return self.get_tile_xy(*tup)

    def get_tile_xy(self, x, y) -> Tile:
        return self.get_tile_pos(Position(x, y))

    def get_tile_pos(self, pos: Position) -> Tile:
        return self.tiles[pos.y][pos.x]

    @property
    def guard(self) -> Guard:
        return self._guard

    @property
    def next_tile_position(self):
        if self.guard.direction == Direction.UP:
            # check tile y-1
            if self.guard.pos.y == 0: return None
            return self.guard.pos.y - 1, self.guard.pos.x
        elif self.guard.direction == Direction.DOWN:
            # check tile y + 1
            if self.guard.pos.y == self.tiles.shape[0] - 1: return None
            return self.guard.pos.y + 1, self.guard.pos.x
        elif self.guard.direction == Direction.LEFT:
            # check tile x - 1
            if self.guard.pos.x == 0: return None
            return self.guard.pos.y, self.guard.pos.x - 1
        elif self.guard.direction == Direction.RIGHT:
            # check tile x + 1
            if self.guard.pos.x == self.tiles.shape[1] - 1: return None
            return self.guard.pos.y, self.guard.pos.x + 1

    @property
    def next_tile(self):
        next_tile_position = self.next_tile_position
        if next_tile_position:
            return self.get_tile_xy(*reversed(next_tile_position))
        return None

    def move_guard(self):
        # Returns True if guard was moved
        # Returns False if guard moved on the tile it previously traveled in the same direction
        # Returns None if guard left the map
        next_tile_position = self.next_tile_position
        if self.next_tile_position:
            if not (self.next_tile.is_obstacle or self.next_tile.is_loop_obstacle):
                next_tile_directions = [direction for direction in self.get_tile_tuple(reversed(next_tile_position)).pass_directions]
                if self.guard.direction in next_tile_directions:
                    return False
                self.guard.set_pos_tuple(reversed(next_tile_position))
            else:
                self.get_tile_pos(self.guard.pos).is_turn_right = True
                self.guard.turn_right()
                # self.guard.set_pos_tuple(reversed(self.next_tile_position))
            self.get_tile_pos(self.guard.pos).pass_directions.append(self.guard.direction)
            return True
        else:
            return None

    def __str__(self):
        return "\n".join(["".join([str(tile) for tile in row]) for row in self.tiles])

    def print(self):
        print(str(self))