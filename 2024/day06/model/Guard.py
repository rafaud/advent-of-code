from .Direction import Direction
from .Position import Position

class Guard:
    def __init__(self, pos: Position, direction: Direction):
        self.pos = pos
        self.direction = direction

    def set_pos_xy(self, x, y):
        self.pos.x = x
        self.pos.y = y

    def set_pos_tuple(self, tup):
        self.pos = Position(*tup)

    def turn_right(self):
        self.direction = self.direction.get_rotated_right()