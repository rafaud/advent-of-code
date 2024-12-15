import copy
import curses

import numpy as np
from Box import Box

class Map:
    def __init__(self):
        self._map_size = {"w": 0, "h": 0}
        self._robot = ()
        self._boxes = []
        self._walls = np.array([])
        # self._map_array = np.array([])
        self._moves = ""
        self._total_moves = 0

    @classmethod
    def load_from_file(cls, path, part=1):
        object = cls()

        data = open(path).read().splitlines()
        partition_index = data.index("")
        padding = 1
        if part == 1:
            padding = 1
            map_array = np.array([list(line) for line in data[:partition_index]])
        else:
            padding = 2
            # replace # with ##
            # replace O with []
            # replace @ with @.
            # replace . with ..
            map_array = np.array([
                list(
                    line.replace("#", "##")
                    .replace("O", "[]")
                    .replace(".", "..")
                    .replace("@", "@.")
                ) for line in data[:partition_index]
            ])

        moves = "".join(data[partition_index + 1:])
        object._map_size = (len(map_array),len(map_array[0]))
        walls = np.full(object.map_size, ".", dtype=str)

        for y, row in enumerate(map_array):
            for x, value in enumerate(row):
                if value == "O":
                    box = Box((y, x), 1)
                    object._boxes.append(box)
                elif value == "[":
                    box = Box((y, x), 2)
                    object._boxes.append(box)
                elif value == "@":
                    object._robot = (y, x)
                    map_array[y, x] = "."
                elif value == "#":
                    walls[y, x] = value

        object._walls = walls
        object._moves = moves
        object._total_moves = len(moves)

        return object
    @property
    def map_size(self):
        return self._map_size

    @property
    def robot(self):
        return self._robot

    @robot.setter
    def robot(self, value):
        self._robot = value

    @property
    def walls(self):
        return self._walls

    @property
    def boxes(self):
        return self._boxes

    @property
    def moves(self):
        return self._moves

    @moves.setter
    def moves(self, value):
        self._moves = value

    @property
    def map_array(self):
        return_value = copy.deepcopy(self.walls)

        for box in self.boxes:
            y, x = box.pos
            for i, ch in enumerate(box.graphics):
                return_value[y, x + i] = ch

        return_value[self.robot] = "@"

        return return_value

    def get_next_move(self):
        next_move = self.moves[0]
        self.moves = self.moves[1:]
        return next_move

    def get_vector_for_direction(self, direction) -> (int, int):
        if direction == "^":
            return -1, 0
        elif direction == "v":
            return 1, 0
        elif direction == "<":
            return 0, -1
        elif direction == ">":
            return 0, 1

    def move(self):
        next_move = self.get_next_move()
        move_vector = self.get_vector_for_direction(next_move)
        next_tile = tuple([sum(value) for value in zip(move_vector, self.robot)])

        if self.walls[*next_tile] == "#":
            return False

        if box := self.get_box_for_tile(next_tile):
            if self.can_box_be_moved(box, next_move):
                self.move_box(box, next_move)
            else:
                return False
        self.robot = next_tile


    def get_box_for_tile(self, tile: (int, int)):
        for box in self.boxes:
            if tile in box.tiles:
                 return box
        return None

    def can_box_be_moved(self, box: Box, direction: str):
        return_value = True
        for next_tile in box.next_tiles(direction):
            if self.walls[*next_tile] == "#":
                 return_value = False
            if next_box := self.get_box_for_tile(next_tile):
                return_value = self.can_box_be_moved(next_box, direction)
            if not return_value:
                return return_value

        return return_value

    def move_box(self, box: Box, direction: str):
        for next_tile in box.next_tiles(direction):
            if next_box := self.get_box_for_tile(next_tile):
                self.move_box(next_box, direction)
        box.move_box(self.get_vector_for_direction(direction))



    def print_map(self, stdscr):
        for y, row in enumerate(self.map_array):
            for x, col in enumerate(row):
                if col == "@":
                    stdscr.addstr(y, x, "@", curses.color_pair(3))
                elif col == "#":
                    stdscr.addstr(y, x, "#", curses.color_pair(1))
                elif col == "O":
                    stdscr.addstr(y, x, "O", curses.color_pair(2))
                elif col == "[":
                    stdscr.addstr(y, x, "[", curses.color_pair(2))
                elif col == "]":
                    stdscr.addstr(y, x, "]", curses.color_pair(2))

    @property
    def map_string(self):
        return "\n".join(["".join(line) for line in self.map_array])

    @property
    def total(self):
        total = 0
        for y, row in enumerate(self.map_array):
            for x, col in enumerate(row):
                if col == "O" or col == "[":
                    total += y * 100 + x

        return total

    @property
    def moves_left(self):
        return len(self.moves)

    @property
    def total_moves(self):
        return self._total_moves