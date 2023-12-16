import sys
sys.path.append('../../../common')
from parser import *

class Sequence:
    def __init__(self, values):
        self.values = values

    def __str__(self):
        return str(self.values)

def get_list_diff(list_values):
    return [list_values[i] - list_values[i - 1] for i in range(1, len(list_values))]

def parse_input_line(input_line):
    return Sequence([int(value) for value in input_line])

def get_next_value_in_sequence(sequence):
    if all([x == 0 for x in sequence.values]):
        return 0
    delta_sequence = Sequence(get_list_diff(sequence.values))
    return sequence.values[-1] + get_next_value_in_sequence(delta_sequence)

def get_previous_value_in_sequence(sequence):
    if all([x == 0 for x in sequence.values]):
        return 0
    delta_sequence = Sequence(get_list_diff(sequence.values))
    return sequence.values[0] - get_previous_value_in_sequence(delta_sequence)

puzzle_input = load_multi_line_input_separated_by_spaces()
sequences = [parse_input_line(input_line) for input_line in puzzle_input]

next_value_total = 0
previous_value_total = 0 
for sequence in sequences:
    next_value_total += get_next_value_in_sequence(sequence)
    previous_value_total += get_previous_value_in_sequence(sequence)
    
print("Part 1: " + str(next_value_total))
print("Part 2: " + str(previous_value_total))

