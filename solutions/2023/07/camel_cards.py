import sys
sys.path.append('../../../common')
from parser import *

from enum import Enum
from sortedcontainers import SortedList

class CardHandType(Enum):
    NONE = 0
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        else:
            return NotImplemented

class Card(Enum):
    JOKER = (1, '?')
    TWO = (2, '2')
    THREE = (3, '3')
    FOUR = (4, '4')
    FIVE = (5, '5')
    SIX = (6, '6')
    SEVEN = (7, '7')
    EIGHT = (8, '8')
    NINE = (9, '9')
    TEN = (10, 'T')
    JACK = (11, 'J')
    QUEEN = (12, 'Q')
    KING = (13, 'K')
    ACE = (14, 'A')

    def __new__(cls, rank, label):
        obj = object.__new__(cls)
        obj._value_ = label
        obj.rank = rank
        return obj

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.rank < other.rank
        else:
            return NotImplemented
    
    @classmethod
    def from_label(cls, label):
        return cls(label)
        

class CardHand:
    def __init__(self, card_list, bid):
        self.card_list = card_list
        self.n_cards = len(card_list)
        self.bid = bid
        card_map = {}
        for card_value in Card:
            card_map[card_value] = 0
        for card in card_list:
            card_map[card] += 1
        self.type = self.__get_hand_type(card_map)
        self.card_map = card_map

    def __eq__(self, other):
        return self.card_list == other.card_list

    def __lt__(self, other):
        if self.type == other.type:
            return self.lt_compare_cards_in_order(other)
        else:
            return self.type < other.type

    def __get_hand_type(self, card_map):
        n_wildcards = card_map[Card.JOKER]
    
        cards_sorted_by_occurrence = sorted(card_map, key=card_map.get, reverse=True)

        first_most_frequent_card = cards_sorted_by_occurrence[0]
        second_most_frequent_card = cards_sorted_by_occurrence[1]
        third_most_frequent_card = cards_sorted_by_occurrence[2]

        if first_most_frequent_card == Card.JOKER:
            n_first_most_frequent_value = card_map[second_most_frequent_card] + n_wildcards
            n_second_most_frequent_value = card_map[third_most_frequent_card]
        else:
            n_first_most_frequent_value = card_map[first_most_frequent_card] + n_wildcards
            n_second_most_frequent_value = card_map[third_most_frequent_card] if second_most_frequent_card == Card.JOKER else card_map[second_most_frequent_card]
        
        if n_first_most_frequent_value >= 5:
            return CardHandType.FIVE_OF_A_KIND
        elif n_first_most_frequent_value >= 4:
            return CardHandType.FOUR_OF_A_KIND
        elif n_first_most_frequent_value >= 3 and n_second_most_frequent_value >= 2:
            return CardHandType.FULL_HOUSE
        elif n_first_most_frequent_value >= 3:
            return CardHandType.THREE_OF_A_KIND
        elif n_first_most_frequent_value >= 2 and n_second_most_frequent_value >= 2:
            return CardHandType.TWO_PAIR
        elif n_first_most_frequent_value >= 2:
            return CardHandType.ONE_PAIR
        else:
            return CardHandType.HIGH_CARD

    def lt_compare_cards_in_order(self, other):
        n_comparisons = min(self.n_cards, other.n_cards)
        for card_index in range(n_comparisons):
            if self.card_list[card_index] < other.card_list[card_index]:
                return True
            elif self.card_list[card_index] > other.card_list[card_index]:
                return False
        return self.n_cards < other.n_cards
        
class CardGame:
    def __init__(self):
        self.card_hands = SortedList()

    def add_card_hand(self, card_hand):
        self.card_hands.add(card_hand)

    def get_total_winnings(self):
        total_winnings_sum = 0
        for idx, card_hand in enumerate(self.card_hands):
            total_winnings_sum += (idx + 1) * card_hand.bid
        return total_winnings_sum
    

def parse_puzzle_input_1(puzzle_input):
    card_game = CardGame()
    for input_line in puzzle_input:
        parts = input_line.split(' ')
        cards = [Card.from_label(label) for label in list(parts[0])]
        bid = int(parts[1])
        card_game.add_card_hand(CardHand(cards, bid))
    return card_game

def parse_puzzle_input_2(puzzle_input):
    card_game = CardGame()
    for input_line in puzzle_input:
        parts = input_line.replace('J','?').split(' ')
        cards = [Card.from_label(label) for label in list(parts[0])]
        bid = int(parts[1])
        card_game.add_card_hand(CardHand(cards, bid))
    return card_game

puzzle_input = load_multi_line_input_as_string_list()

card_game_1 = parse_puzzle_input_1(puzzle_input)
print("Part 1: " + str(card_game_1.get_total_winnings()))

card_game_2 = parse_puzzle_input_2(puzzle_input)
print("Part 1: " + str(card_game_2.get_total_winnings()))
