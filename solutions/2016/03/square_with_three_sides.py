import sys
sys.path.append('../../../common')
from parser import *
import copy

puzzle_input = load_multi_line_input_separated_by_spaces()

def process_puzzle_input_line(line):
    sides = [int(s) for s in line]
    return sides

def can_be_triangle(sides):
    sorted_sides = sorted(sides)
    return sorted_sides[2] < sorted_sides[0] + sorted_sides[1]


def count_potention_triangles(sides_set):
    n_potential_triangles = 0
    for sides in sides_set:
        if can_be_triangle(sides):
            n_potential_triangles += 1
    return n_potential_triangles

def get_column_grouped_values(list_of_lists, n_grouping):
    result = []
    for current_col in range(len(list_of_lists[0])):
        for current_row_start in range(0, len(list_of_lists), n_grouping):
            grouping = []
            for row in range(current_row_start, current_row_start + n_grouping):
                grouping.append(list_of_lists[row][current_col])
            result.append(grouping)
    return result

n_potential_triangles = 0
listed_sides = []
for line in puzzle_input:
    listed_sides.append(process_puzzle_input_line(line))

print("Part 1: " + str(count_potention_triangles(listed_sides)))
new_sides = get_column_grouped_values(listed_sides, 3)
print("Part 2: " + str(count_potention_triangles(new_sides)))
