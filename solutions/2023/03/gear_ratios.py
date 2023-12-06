import sys
sys.path.append('../../../common')
from str_util import *
from parser import *
from grid import *

class EngineSchematicNumber:
    def __init__(self):
        self.str_value = ''
        self.grid_positions = set()

    def append_str_value(self, c, position):
        self.str_value += c
        self.grid_positions.add(position)

    def __str__(self):
        return self.str_value + "@" + list_as_string_repr(self.grid_positions)

    def is_adjacent_to_position(self, other_grid_position):
        return any([number_position.is_diagonally_or_directly_adjacent(other_grid_position) for number_position in self.grid_positions])

class EngineSchematicSymbol:
    def __init__(self, value, grid_position):
        self.value = value
        self.grid_position = grid_position

    def __str__(self):
        return "'" + self.value + "'@" + str(self.grid_position)

class EngineGear:
    def __init__(self, grid_position, adjacent_numbers):
        self.grid_position = grid_position
        self.adjacent_numbers = adjacent_numbers

    def get_gear_ratio(self):
        return int(self.adjacent_numbers[0].str_value) * int(self.adjacent_numbers[1].str_value)

class EngineSchematic:
    def __init__(self):
        self.numbers = []
        self.symbols = []

    def add_number(self, engine_schematic_number):
        self.numbers.append(engine_schematic_number)

    def add_symbol(self, engine_schematic_symbol):
        self.symbols.append(engine_schematic_symbol)

    def get_gears(self):
        gears = []
        for symbol in self.symbols:
            if symbol.value != '*':
                continue
            adjacent_numbers = []
            for number in self.numbers:
                if number.is_adjacent_to_position(symbol.grid_position):
                    adjacent_numbers.append(number)
            if len(adjacent_numbers) == 2:
                gears.append(EngineGear(symbol.grid_position, adjacent_numbers))
        return gears
            
    
def process_puzzle_input_line(engine_schematic, input_line, row_number):
    current_number = None
    for col_n in range(len(input_line)):
        current_char = input_line[col_n]
        if current_char.isnumeric():
            if current_number is None:
                current_number = EngineSchematicNumber()
                engine_schematic.add_number(current_number)
            current_number.append_str_value(current_char, GridPosition(row_number, col_n))
        else:
            if current_number is not None:
                current_number = None
            if current_char == '.':
                continue
            else:
                engine_schematic.add_symbol(EngineSchematicSymbol(current_char, GridPosition(row_number, col_n)))
            

puzzle_input = load_multi_line_input_as_character_arrays()
engine_schematic = EngineSchematic()
for row_n in range(len(puzzle_input)):
    process_puzzle_input_line(engine_schematic, puzzle_input[row_n], row_n)
    
engine_part_sum = 0
for number in engine_schematic.numbers:
    for symbol in engine_schematic.symbols:
        if number.is_adjacent_to_position(symbol.grid_position):
            engine_part_sum += int(number.str_value)
            break
        
gear_ratio_sum = sum([gear.get_gear_ratio() for gear in engine_schematic.get_gears()])

print("Part 1: " + str(engine_part_sum))
print("Part 2: " + str(gear_ratio_sum))
