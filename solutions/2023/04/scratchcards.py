import sys
sys.path.append('../../../common')
from str_util import *
from parser import *

class ScratchCard:
    def __init__(self, card_id, chosen_numbers, winning_numbers):
        self.card_id = card_id
        self.chosen_numbers = chosen_numbers
        self.winning_numbers = winning_numbers

    def get_matching_numbers(self):
        return [number for number in self.chosen_numbers if number in self.winning_numbers]

    def get_points(self):
        n_matches = len(self.get_matching_numbers())
        return 2 ** (n_matches - 1) if n_matches > 0 else 0
        
def parse_number_list(number_list):
    return [int(n.strip()) for n in number_list.split(' ') if len(n) != 0]

def parse_input_line(input_line):
    parts = input_line.split(':')
    number_parts = parts[1].split('|')
    
    card_id = int(parts[0][4:].strip())
    chosen_numbers = parse_number_list(number_parts[0])
    winning_numbers = parse_number_list(number_parts[1])

    return ScratchCard(card_id, chosen_numbers, winning_numbers)

puzzle_input = load_multi_line_input_as_string_list()
scratch_cards = [parse_input_line(input_line) for input_line in puzzle_input]
total_points = sum([scratch_card.get_points() for scratch_card in scratch_cards])

# Part 2
scratch_card_to_total = {}
def get_total_scratchcards(scratch_card_id):
    if scratch_card_id in scratch_card_to_total:
        return scratch_card_to_total[scratch_card_id]
    else:
        # Scratch cards were stored in order in scratch_cards (with index shifted -1)
        scratch_card = scratch_cards[scratch_card_id - 1]
        total_scratchcards = 1 # Including the current card
        n_matches = len(scratch_card.get_matching_numbers())
        for next_scratchcard_id in range(scratch_card_id + 1, scratch_card_id + 1 + n_matches):
            total_scratchcards += get_total_scratchcards(next_scratchcard_id)
        scratch_card_to_total[scratch_card_id] = total_scratchcards
        return total_scratchcards

scratch_card_count = sum([get_total_scratchcards(scratch_card_id) for scratch_card_id in range(1, len(scratch_cards) + 1)])

print("Part 1: " + str(total_points))
print("Part 2: " + str(scratch_card_count))
