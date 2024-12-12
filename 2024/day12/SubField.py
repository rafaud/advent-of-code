import typing
from uuid import uuid4

import numpy as np


class SubField(object):
    def __init__(self, field_type: str):
        self._uuid = uuid4()
        self._field_type = field_type
        self._tiles = set()
        self._size = (0, 0)

    def get_representation(self, field_shape: tuple[int, int] = None) -> np.ndarray:
        if field_shape is None:
            field_shape = self._size
        if field_shape[0] < self._size[0]:
            field_shape = (self._size[0], field_shape[1])
        if field_shape[1] < self._size[1]:
            field_shape = (field_shape[0], self._size[1])

        field = np.array([["." for _ in range(field_shape[1])] for _ in range(field_shape[0])])
        for tile in self._tiles:
            field[*tile] = self._field_type
        return field

    def get_string_representation(self, field_shape: tuple[int, int] = None) -> str:
        representation = self.get_representation(field_shape)
        return "\n".join(["".join(row) for row in representation])

    @property
    def tiles(self):
        return self._tiles

    def add_tile(self, tile: tuple[int, int]):
        if tile[0]+1 > self._size[0]:
            self._size = (tile[0]+1, self._size[1])
        if tile[1]+1 > self._size[1]:
            self._size = (self._size[0], tile[1]+1)

        self._tiles.add(tile)

    def add_tiles(self, tiles: [tuple[int, int]]):
        for tile in tiles:
            self.add_tile(tile)

    @property
    def uuid(self):
        return self._uuid

    @property
    def field_type(self):
        return self._field_type

    @property
    def size(self):
        return self._size

    @property
    def area(self):
        return len(self._tiles)

    @property
    def perimeter(self):
        perimeter = 0
        for tile in self._tiles:
            perimeter += 4 - self.get_neighbour_count(tile)
        return perimeter


    def get_fence_cost(self, discount: bool = False):
        if discount:
            return self.area * self.get_corner_count()
        else:
            return self.area * self.perimeter

    def get_neighbour_count(self, tile_coords: tuple[int, int]) -> int:

        row = tile_coords[0]
        col = tile_coords[1]

        neighbours_count = 0

        # check tile north
        neighbour_coords = (row - 1, col)
        if neighbour_coords in self._tiles:
            neighbours_count += 1

        # check tile east
        neighbour_coords = (row, col + 1)
        if neighbour_coords in self._tiles:
            neighbours_count += 1

        # check tile south
        neighbour_coords = (row + 1, col)
        if neighbour_coords in self._tiles:
            neighbours_count += 1

        # check tile west
        neighbour_coords = (row, col - 1)
        if neighbour_coords in self._tiles:
            neighbours_count += 1

        return neighbours_count


    def get_corner_count(self) -> int:
        corners = 0
        representation = self.get_representation()
        representation = np.pad(representation, ((1, 1), (1, 1)), constant_values='.')
        for row in range(self.size[0] + 1):
            for col in range(self.size[1] + 1):
                representation_slice = representation[row:row+2, col:col+2]
                empty_spaces = sum(foo == "." for row in representation_slice for foo in row)
                if empty_spaces == 1 or empty_spaces == 3:
                    corners += 1
                elif empty_spaces == 2:
                    if representation_slice[0, 0] == representation_slice[1, 1]:
                        # super edge case of:
                        #  . A
                        #  A .
                        # being one region
                        corners += 2

        return corners


    @classmethod
    def get_neighbour(cls, tile_coords: tuple[int, int], field: np.ndarray) -> [tuple[int, int]]:
        field_shape = field.shape
        tile_type = field[*tile_coords]

        row = tile_coords[0]
        col = tile_coords[1]

        neighbours = []

        # check tile north
        neighbour_coords = (row - 1, col)
        if SubField.is_in_bounds(neighbour_coords, field_shape):
            if field[*neighbour_coords] == tile_type:
                neighbours.append(neighbour_coords)
        # check tile east
        neighbour_coords = (row, col + 1)
        if SubField.is_in_bounds(neighbour_coords, field_shape):
            if field[*neighbour_coords] == tile_type:
                neighbours.append(neighbour_coords)
        # check tile south
        neighbour_coords = (row + 1, col)
        if SubField.is_in_bounds(neighbour_coords, field_shape):
            if field[*neighbour_coords] == tile_type:
                neighbours.append(neighbour_coords)
        # check tile west
        neighbour_coords = (row, col - 1)
        if SubField.is_in_bounds(neighbour_coords, field_shape):
            if field[*neighbour_coords] == tile_type:
                neighbours.append(neighbour_coords)

        return neighbours

    @classmethod
    def is_in_bounds(cls, _tile_coords: tuple[int, int], field_shape: tuple[int, int]) -> bool:
        _row = _tile_coords[0]
        _col = _tile_coords[1]
        return 0 <= _row < field_shape[0] and 0 <= _col < field_shape[1]

    @classmethod
    def merge_subfields(cls, sub_fields: [typing.Self]) -> typing.Self:
        new_sub_field = SubField(sub_fields[0].field_type)
        for sub_field in sub_fields:
            new_sub_field.add_tiles(sub_field.tiles)

        return new_sub_field