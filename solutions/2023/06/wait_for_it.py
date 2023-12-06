import sys
sys.path.append('../../../common')
from parser import *

import math

class Race:
    def __init__(self, distance, time):
        self.distance = distance
        self.time = time
        exact_button_times = solve_for_exact_button_times(distance, time)
        self.winning_combinations = get_number_of_winning_combinations(exact_button_times)

    def __str__(self):
        return "Race=" + str(self.distance) + "/" + str(self.time)

import re

def parse_puzzle_input_1(puzzle_input):
    races = []
    times = [int(time_text) for time_text in re.split("\s+", puzzle_input[0])[1:]]
    distances = [int(distance_text) for distance_text in re.split("\s+", puzzle_input[1])[1:]]
    for i in range(len(times)):
        races.append(Race(distances[i], times[i]))
    return races

def parse_puzzle_input_2(puzzle_input):
    time = int(''.join(re.split("\s+", puzzle_input[0])[1:]))
    distance = int(''.join(re.split("\s+", puzzle_input[1])[1:]))
    return Race(distance, time)

def solve_for_exact_button_times(dist, time):
    # Solving for x * (t - x) - d = 0 which comes to x = +/- (sqrt(t^2/4 - d)) + t/2
    inner_expression = (time**2 / 4) - dist
    if inner_expression < 0:
        return []
    elif inner_expression == 0:
        return [time/2]
    else:
        return [-(inner_expression**0.5) + time/2, inner_expression**0.5 + time/2]

def get_number_of_winning_combinations(exact_button_times):
    if len(exact_button_times) == 0:
        return 0 # Should not occur
    elif len(exact_button_times) == 1:
        return 1 if exact_button_times[0].is_integer() else 0
    else:
        # Return the number of integers between the solutions
        return math.ceil(exact_button_times[1]) - math.floor(exact_button_times[0] + 1)

races_1 = parse_puzzle_input_1(load_multi_line_input_as_string_list())
product_1 = 1
for r in races_1:
    product_1 *= r.winning_combinations

race_2 = parse_puzzle_input_2(load_multi_line_input_as_string_list())

print("Part 1: " + str(product_1))
print("Part 2: " + str(race_2.winning_combinations))

