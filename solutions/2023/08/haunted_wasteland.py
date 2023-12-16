import sys
sys.path.append('../../../common')
from parser import *
from str_util import *

import re
import math

class LRNode:
    def __init__(self, node_id, left_node_id, right_node_id):
        self.node_id = node_id
        self.adjacent_nodes = {}
        self.adjacent_nodes['L'] = left_node_id
        self.adjacent_nodes['R'] = right_node_id

    def is_starting_node(self):
        return list(self.node_id)[-1] == 'A'

    def is_ending_node(self):
        return list(self.node_id)[-1] == 'Z'

    def __eq__(self, other):
        return self.node_id == other.node_id

    def __hash__(self):
        return hash(self.node_id)

    def __str__(self):
        return "LRNode[" + self.node_id + "]"

class LeftRightNetwork:
    def __init__(self):
        self.nodes_map = {}
        self.starting_nodes = set()

    def add_node(self, lr_node):
        self.nodes_map[lr_node.node_id] = lr_node
        if lr_node.is_starting_node():
            self.starting_nodes.add(lr_node)

    def get_node(self, node_id):
        return self.nodes_map[node_id]

def parse_puzzle_input(puzzle_input):
    lr_instruction_sequence = list(puzzle_input[0])
    lr_network = LeftRightNetwork()
    for input_line in puzzle_input[2:]:
        simplified_line = remove_chars_from_string(input_line, [' ', '(', ')'])
        parts = re.split(',|=', simplified_line)
        lr_node = LRNode(parts[0], parts[1], parts[2])
        lr_network.add_node(lr_node)
    return lr_instruction_sequence, lr_network


puzzle_input = load_multi_line_input_as_string_list()
lr_instruction_sequence, lr_network = parse_puzzle_input(puzzle_input)


n_steps_1 = 0
current_node_1 = lr_network.get_node("AAA")
while current_node_1.node_id != "ZZZ":
    current_instruction = lr_instruction_sequence[n_steps_1 % len(lr_instruction_sequence)]
    next_node_id = current_node_1.adjacent_nodes[current_instruction]
    current_node_1 = lr_network.get_node(next_node_id)
    n_steps_1 += 1

print("Part 1: " + str(n_steps_1))


class NodeCycleInfo:
    def __init__(self, cycle_start_shift, cycle_length, pre_cycle_match_indices, on_cycle_match_indices):
        self.cycle_start_shift = cycle_start_shift
        self.cycle_length = cycle_length
        self.pre_cycle_match_indices = pre_cycle_match_indices
        self.on_cycle_match_indices = on_cycle_match_indices

    def __str__(self):
        return "NodeCycleInfo:_shift=" + str(self.cycle_start_shift) + ",length=" + str(self.cycle_length) + ",pre-cycle-matches=" + str(self.pre_cycle_match_indices) + ",on-cycle-matches=" + str(self.on_cycle_match_indices)

    def get_zero_shifted_cycle_values(self):
        return sorted([(index + self.cycle_start_shift) % self.cycle_length for index in self.on_cycle_match_indices])
        
def get_ending_node_cycles(lr_network, lr_instruction_sequence, starting_node):
    current_node = starting_node
    n_steps = 0
    instruction_index = 0
    visited_states = {} #State is the current node and the next sequence index
    ending_node_indices = []
    while not (current_node, instruction_index) in visited_states:
        visited_states[(current_node, instruction_index)] = n_steps
        if current_node.is_ending_node():
            ending_node_indices.append(n_steps)
        current_instruction = lr_instruction_sequence[instruction_index]
        current_node = lr_network.get_node(current_node.adjacent_nodes[current_instruction])
        n_steps += 1
        instruction_index = n_steps % len(lr_instruction_sequence)
        
    # Cycle has occurred - cycle starts when we originally hit this state and ends on the current step
    cycle_start_shift = visited_states[(current_node, instruction_index)]
    cycle_length = n_steps - cycle_start_shift
    pre_cycle_match_indices = [i for i in ending_node_indices if i < cycle_start_shift]
    on_cycle_match_indices = [i for i in ending_node_indices if i >= cycle_start_shift]
    return NodeCycleInfo(cycle_start_shift, cycle_length, pre_cycle_match_indices, on_cycle_match_indices)


def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

def lcm_multi(values):
    if len(values) == 2:
        return lcm(values[0], values[1])
    return lcm_multi([lcm(values[0], values[1])] + values[2:])

starting_nodes = list(lr_network.starting_nodes)
node_cycle_infos = [get_ending_node_cycles(lr_network, lr_instruction_sequence, starting_node) for starting_node in starting_nodes]

# From above we have the values printed [print(str(node_cycle_infos))] and they happen to occur in cycles on the index that matches the cycle length

print("Part 2: " + str(lcm_multi([21409, 15989, 14363, 11653, 12737, 19241])))
