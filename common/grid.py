from enum import Enum

class GridDirection(Enum):
    UP = "UP"
    RIGHT = "RIGHT"
    DOWN = "DOWN"
    LEFT = "LEFT"

class FiniteGrid:
    def __init__(self, n_x, n_y):
        self.n_x = n_x
        self.n_y = n_y

    def is_position_on_grid(self, position):
        return position.x in range(self.n_x) and position.y in range(self.n_y)

class FiniteIrregularGrid:
    def __init__(self, valid_positions):
        self.valid_positions = valid_positions

    def is_position_on_grid(self, position):
        return position in self.valid_positions


class GridPosition:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return 11 * self.x + 17 * self.y

    def __str__(self):
        return "[x:" + str(self.x) + ",y:" + str(self.y) + "]"

    def position_at_dx(self, dx):
        return GridPosition(self.x + dx, self.y)

    def position_at_dy(self, dy):
        return GridPosition(self.x, self.y + dy)

    def manhattan_distance_from_origin(self):
        return abs(self.x) + abs(self.y)

    def manhattan_distance_from_other(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def is_diagonally_or_directly_adjacent(self, other):
        return True if abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1 and self != other else False

class GridPose:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

    def __eq__(self, other):
        return self.position == other.position and self.direction == other.direction

    def __hash__(self):
        return hash(self.position) + hash(self.direction)

    def __str__(self):
        return str(self.position) + "->" + str(self.direction.value)

    def pose_rotate_clockwise(self):
        match self.direction:
            case GridDirection.UP:
                new_direction = GridDirection.RIGHT
            case GridDirection.RIGHT:
                new_direction = GridDirection.DOWN
            case GridDirection.DOWN:
                new_direction = GridDirection.LEFT
            case GridDirection.LEFT:
                new_direction = GridDirection.UP
        return GridPose(self.position, new_direction)
    
    def pose_rotate_counter_clockwise(self):
        match self.direction:
            case GridDirection.UP:
                new_direction = GridDirection.LEFT
            case GridDirection.RIGHT:
                new_direction = GridDirection.UP
            case GridDirection.DOWN:
                new_direction = GridDirection.RIGHT
            case GridDirection.LEFT:
                new_direction = GridDirection.DOWN
        return GridPose(self.position, new_direction)

    def pose_move_in_current_direction(self, displacement):
        match self.direction:
            case GridDirection.UP:
                new_position = self.position.position_at_dy(displacement)
            case GridDirection.RIGHT:
                new_position = self.position.position_at_dx(displacement)
            case GridDirection.DOWN:
                new_position = self.position.position_at_dy(-displacement)
            case GridDirection.LEFT:
                new_position = self.position.position_at_dx(-displacement)
        return GridPose(new_position, self.direction)
