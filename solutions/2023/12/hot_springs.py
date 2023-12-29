import sys
sys.path.append('../../../common')
from parser import *

SPRING = '#'
EMPTY = '.'
UNKNOWN = '?'

def parse_expected_contigious_springs(text):
    return [int(value) for value in text.split(',')]


class HotSpringArrangementCountSolver:

    #
    def __init__(self):
        self.solution_map = {}

    def solve(self, records, expected_contiguous_springs):
        return self.__count_possible_hot_spring_arrangements(records, expected_contiguous_springs)


    def __count_possible_hot_spring_arrangements(self, records, expected_contiguous_springs):
        # Check if same configuration has already been counted
        key = self.__get_key(records, expected_contiguous_springs)
        if key in self.solution_map:
            return self.solution_map[key]

        return_value = None
        if len(expected_contiguous_springs) == 0:
            if SPRING in records:
                return_value = 0
            else:
                return_value = 1
        elif len(records) == 0 and len(expected_contiguous_springs) !=0:
            return_value = 0
        else:
            current_char = records[0] # This cannot be empty
            if current_char == EMPTY:
                return_value = self.__count_possible_hot_spring_arrangements(records[1:], expected_contiguous_springs)
            if current_char == SPRING:
                # To be valid the next set must not be empty and the one after must not be a spring (and needs to be assumed empty)
                required_spring_count = expected_contiguous_springs[0]
                if len(records) < required_spring_count or EMPTY in records[:required_spring_count] or (len(records) > required_spring_count and SPRING == records[required_spring_count]):
                    return_value = 0
                else:
                    return_value = self.__count_possible_hot_spring_arrangements(records[required_spring_count+1:], expected_contiguous_springs[1:])
            if current_char == UNKNOWN:
                return_value = self.__count_possible_hot_spring_arrangements('#' + records[1:], expected_contiguous_springs) + self.__count_possible_hot_spring_arrangements('.' + records[1:], expected_contiguous_springs)
        self.solution_map[key] = return_value
        return return_value
    
    @staticmethod
    def __get_key(records, expected_contiguous_springs):
        return (records, tuple(expected_contiguous_springs))
        


puzzle_input = load_multi_line_input_separated_by_spaces()
total_combinations_1 = 0
total_combinations_2 = 0
for input_line in puzzle_input:
    hsacs = HotSpringArrangementCountSolver()
    records_1 = input_line[0]
    records_2 = '?'.join([records_1] * 5)
    expected_contiguous_springs_1 = parse_expected_contigious_springs(input_line[1])
    expected_contiguous_springs_2 = expected_contiguous_springs_1 * 5
    total_combinations_1 += hsacs.solve(records_1, expected_contiguous_springs_1)
    total_combinations_2 += hsacs.solve(records_2, expected_contiguous_springs_2)

print("Part 1: " + str(total_combinations_1))
print("Part 2: " + str(total_combinations_2))

