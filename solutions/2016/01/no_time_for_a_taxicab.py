import sys
sys.path.append('../../../common')
from grid import *
from parser import *
from enum import Enum
    
puzzle_input = load_single_line_input([' ', '\n'], [','])
pose = GridPose(GridPosition(0, 0), GridDirection.UP)
first_position_visited_twice = None
positions_visited = set()
positions_visited.add(pose.position)
for pi in puzzle_input:
    turning_direction_char = pi[0]
    if turning_direction_char == 'R':
        pose = pose.pose_rotate_clockwise()
    elif turning_direction_char == 'L':
        pose = pose.pose_rotate_counter_clockwise()
    else:
        raise Exception("Invalid turning direction from puzzle input:" + turning_direction_char)
    steps_to_move = int(pi[1:])
    for i in range(steps_to_move):
        pose = pose.pose_move_in_current_direction(1)
        if first_position_visited_twice is None and pose.position in positions_visited:
            first_position_visited_twice = pose.position
        positions_visited.add(pose.position)

print("Part 1:" + str(pose.position.manhattan_distance_from_origin()))
print("Part 2:" + str(first_position_visited_twice.manhattan_distance_from_origin()))
