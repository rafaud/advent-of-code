from .Direction import Direction

class Tile:
    def __init__(self):
        self.is_obstacle = False
        self.is_starting_position = False
        self.is_loop_obstacle = False
        self.pass_directions = []
        self.is_turn_right = False
        self.error = False

    @property
    def is_vertical(self):
        return Direction.UP in self.pass_directions or Direction.DOWN in self.pass_directions

    @property
    def is_horizontal(self):
        return Direction.LEFT in self.pass_directions or Direction.RIGHT in self.pass_directions

    @property
    def is_horizontal_and_vertical(self):
        return self.is_vertical and self.is_horizontal

    @property
    def is_passed(self):
        if self.pass_directions:
            return  True
        return False

    def __str__(self):
        if self.error:
            return 'X'
        if self.is_starting_position:
            return "▲"
        if self.is_obstacle:
            return "■"
        if self.is_loop_obstacle:
            return "○"

        if self.is_turn_right:
            if self.pass_directions[0] == Direction.UP:
                return "╔"
            elif self.pass_directions[0] == Direction.RIGHT:
                return "╗"
            elif self.pass_directions[0] == Direction.DOWN:
                return "╝"
            elif self.pass_directions[0] == Direction.LEFT:
                return "╚"

        if self.is_horizontal_and_vertical:
            return "╬"
        elif self.is_horizontal:
            return "═"
        elif self.is_vertical:
            return "║"

        return "░"
