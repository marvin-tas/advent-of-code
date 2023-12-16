import sys
sys.path.append('../../../common')
from parser import *
from grid import *

from enum import Enum
import queue

class PipeType(Enum):
    VERTICAL = ('|', [GridDisplacement(0, 1), GridDisplacement(0,-1)])
    HORIZONTAL = ('-', [GridDisplacement(1, 0), GridDisplacement(-1, 0)])
    BEND_NE = ('L', [GridDisplacement(0, 1), GridDisplacement(1, 0)])
    BEND_NW = ('J', [GridDisplacement(0, 1), GridDisplacement(-1, 0)])
    BEND_SE = ('F', [GridDisplacement(0, -1), GridDisplacement(1, 0)])
    BEND_SW = ('7', [GridDisplacement(0, -1), GridDisplacement(-1, 0)])
    STARTING = ('S', [GridDisplacement(0, 1), GridDisplacement(0,-1), GridDisplacement(1, 0), GridDisplacement(-1, 0)])

    def __new__(cls, label, connection_displacements):
        obj = object.__new__(cls)
        obj._value_ = label
        obj.connection_displacements = connection_displacements
        return obj
    
    @classmethod
    def from_label(cls, label):
        return cls(label)
    
class Pipe:
    def __init__(self, grid_position, pipe_type):
        self.grid_position = grid_position
        self.pipe_type = pipe_type

    def is_directly_connected_to_pipe(self, other):
        displacement_to_other = self.grid_position.displacement_to_other(other.grid_position)
        return True if displacement_to_other in self.pipe_type.connection_displacements and -displacement_to_other in other.pipe_type.connection_displacements else False

    def __eq__(self, other):
        return self.grid_position == other.grid_position and self.pipe_type == other.pipe_type

    def __hash__(self):
        return 11 * hash(self.grid_position) + 17 * hash(self.pipe_type)

    def __str__(self):
        return self.pipe_type.value + '@' + str(self.grid_position)

    def __repr__(self):
        return str(self)

class PipeNetwork:
    def __init__(self):
        self.position_to_pipe = {}
        self.starting_pipe = None

    def add_pipe(self, pipe):
        if pipe.pipe_type == PipeType.STARTING:
            self.starting_pipe = pipe
        self.position_to_pipe[pipe.grid_position] = pipe

    def get_directly_connected_pipes(self, pipe):
        connected_pipes = []
        current_position = pipe.grid_position
        connection_positions = [current_position.position_at_displacement(displacement) for displacement in pipe.pipe_type.connection_displacements]
        for connection_position in connection_positions:
            if connection_position not in self.position_to_pipe:
                continue
            other_pipe = self.position_to_pipe[connection_position]
            if other_pipe.grid_position.displacement_to_other(pipe.grid_position) in other_pipe.pipe_type.connection_displacements:
                connected_pipes.append(other_pipe)
        return connected_pipes
    
    def get_circuit_from_starting_pipe(self):
        # Note - we will miss the first right turn if it is one, that is okay because a RHS circuit will have 4 and a LHS will have -4 (so we can miss one and still know)
        right_hand_turn_counter = 0

        starting_pipe = pipe_network.starting_pipe
        connected_pipes = self.get_directly_connected_pipes(starting_pipe)
        previous_pipe = starting_pipe
        current_pipe = connected_pipes[0] # Just choose any first.
        circuit = [starting_pipe, current_pipe]
        while True:
            connected_pipes = self.get_directly_connected_pipes(current_pipe)
            next_pipes = [pipe for pipe in connected_pipes if pipe is not previous_pipe]
            if len(next_pipes) != 1:
                # Either dead end or more than 1 option
                print("Invalid number of options to be a circuit: " + str(len(next_pipes)))
                return None
            next_pipe = next_pipes[0]
            # here we can look at the previous and determine if the turn is right handed for part 2
            previous_displacement = previous_pipe.grid_position.displacement_to_other(current_pipe.grid_position)
            current_displacement = current_pipe.grid_position.displacement_to_other(next_pipe.grid_position)
            right_hand_turn_counter += current_displacement.right_of_other(previous_displacement)
            if next_pipe == starting_pipe:
                if right_hand_turn_counter < 0:
                    # Return equivalent circuit oriented the other way
                    return [circuit[0]] + circuit[:0:-1]
                else:
                    return circuit
            previous_pipe = current_pipe
            current_pipe = next_pipe
            circuit.append(next_pipe)
        return None

        
    def add_empty_position(self, position):
        self.empty_positions.add(position)

def is_position_inside_pipe_circuit(pipe_rhs_circuit, position):
        # Assumes circuit has more right turns than left

        # First find the pipe above the position - if there is none, then the position is definitely outside the circuit
        pipe_directly_above = None, None
        for index in range(len(pipe_rhs_circuit)):
            pipe = pipe_rhs_circuit[index]
            pipe_position = pipe.grid_position
            if pipe_position.x == position.x and pipe_position.y >= position.y:
                if pipe_directly_above[0] is None or pipe_directly_above[0].grid_position.y > pipe_position.y:
                    pipe_directly_above = pipe, index   
        if pipe_directly_above[0] is None:
            return False
        if pipe_directly_above[0].grid_position == position:
            return False
        # Need to determine if the pipe is running left-to-right or right-to-left
        # Either the previous pipe is at the same level - or the next is at the same level. Can take the dx between previous and next
        previous_above_pipe = pipe_rhs_circuit[(pipe_directly_above[1] - 1) % len(pipe_rhs_circuit)]
        next_above_pipe =  pipe_rhs_circuit[(pipe_directly_above[1] + 1) % len(pipe_rhs_circuit)]
        horizontal_displacement = previous_above_pipe.grid_position.displacement_to_other(next_above_pipe.grid_position).dx
        return horizontal_displacement > 0
        
def parse_puzzle_input(puzzle_input):
    pipe_network = PipeNetwork()
    n_rows = len(puzzle_input)
    n_cols = len(puzzle_input[0])
    for row_n in range(len(puzzle_input)):
        current_row = puzzle_input[row_n]
        for col_n in range(len(current_row)):
            value = puzzle_input[row_n][col_n]
            current_position = GridPosition(col_n, row_n)
            if value == '.':
                continue
            pipe = Pipe(current_position, PipeType.from_label(value))
            pipe_network.add_pipe(pipe)
    return pipe_network, n_rows, n_cols
            
puzzle_input = load_multi_line_input_as_character_arrays()
puzzle_input.reverse()
pipe_network, n_rows, n_cols = parse_puzzle_input(puzzle_input)
starting_circuit = pipe_network.get_circuit_from_starting_pipe()

print("Part 1: " + str(len(starting_circuit)//2))

empty_positions_inside_starting_circuit = 0
for r in range(n_rows):
    for c in range(n_cols):
        position = GridPosition(c, r)
        if is_position_inside_pipe_circuit(starting_circuit, position):
            empty_positions_inside_starting_circuit += 1

print("Part 2: " + str(empty_positions_inside_starting_circuit))

