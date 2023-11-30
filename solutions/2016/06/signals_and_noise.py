import sys
sys.path.append('../../../common')
from parser import *

puzzle_input = load_multi_line_input_as_character_arrays()

n_cols = len(puzzle_input[0])
column_count_maps = [{} for i in range(n_cols)]
for line in puzzle_input:
    for i in range(n_cols):
        value = line[i]
        if value not in column_count_maps[i]:
            column_count_maps[i][value] = 1
        else:
            column_count_maps[i][value] += 1
            
message_1 = ""
for column_count in column_count_maps:
    message_1 += max(column_count, key=column_count.get)

print("Part 1: " + message_1)

message_2 = ""
for column_count in column_count_maps:
    message_2 += min(column_count, key=column_count.get)

print("Part 2: " + message_2)
