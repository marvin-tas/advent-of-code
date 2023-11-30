import sys
sys.path.append('../../../common')
from parser import *
from grid import *

def get_button_on_position(position):
    return str(((2 - position.y) * 3) + position.x + 1)

def get_code_positions(button_grid, starting_position, sequence_set):
    position = starting_position
    code_positions = []
    for sequence in sequence_set:
        for direction in sequence:
            match direction:
                case 'U':
                    next_position = position.position_at_dy(1)
                case 'R':
                    next_position = position.position_at_dx(1)
                case 'D':
                    next_position = position.position_at_dy(-1)
                case 'L':
                    next_position = position.position_at_dx(-1)
            if button_grid.is_position_on_grid(next_position):
                position = next_position
        code_positions.append(position)
    return code_positions
    

puzzle_input = load_multi_line_input_as_character_arrays()
#puzzle_input = [['U','L','L'],['R','R','D','D','D'],['L','U','R','D','L'],['U','U','U','U','D']]

button_grid = FiniteGrid(3, 3)
position = GridPosition(1, 1) #starting position
code = [get_button_on_position(pos) for pos in get_code_positions(button_grid, position, puzzle_input)]

print("Part 1: " + "".join(code))

position_to_button_map = {
    GridPosition(0, 2): '5',
    GridPosition(1, 1): 'A',
    GridPosition(1, 2): '6',
    GridPosition(1, 3): '2',
    GridPosition(2, 0): 'D',
    GridPosition(2, 1): 'B',
    GridPosition(2, 2): '7',
    GridPosition(2, 3): '3',
    GridPosition(2, 4): '1',
    GridPosition(3, 1): 'C',
    GridPosition(3, 2): '8',
    GridPosition(3, 3): '4',
    GridPosition(4, 2): '9'
}

def get_button_on_position_2(position):
    return position_to_button_map[position]

button_grid_2 = FiniteIrregularGrid(position_to_button_map.keys())
position_2 = GridPosition(0, 2) #starting position
code_2 = [get_button_on_position_2(pos) for pos in get_code_positions(button_grid_2, position_2, puzzle_input)]

print("Part 2: " + "".join(code_2))
