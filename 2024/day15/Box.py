class Box:
    def __init__(self, pos: (int, int), size: int):
        self._pos = pos
        self._size = max(size, 1)

    @property
    def pos(self):
        return self._pos

    @property
    def size(self):
        return self._size

    @property
    def graphics(self):
        if self.size == 1:
            return "O"
        elif self.size == 2:
            return "[]"

    @property
    def tiles(self):
        y, x = self.pos
        return [(y, x + i) for i in range(self.size)]

    def next_tiles(self, direction):
        tiles = self.tiles
        if direction == "^":
            return [(y - 1, x) for y, x in tiles]
        elif direction == "v":
            return [(y + 1, x) for y, x in tiles]
        elif direction == "<":
            y, x = tiles[0]
            return [(y, x - 1)]
        elif direction == ">":
            y, x = tiles[-1]
            return [(y, x + 1)]

    def move_box(self, vector):
        self._pos = tuple([sum(value) for value in zip(vector, self.pos)])

