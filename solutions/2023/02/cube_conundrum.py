import sys
sys.path.append('../../../common')
from parser import *

class CubeReveal:
    def __init__(self):
        self.red = 0
        self.green = 0
        self.blue = 0

    def get_value_for_colour(self, colour):
        if colour == "red":
            return self.red
        elif colour == "green":
            return self.green
        elif colour == "blue":
            return self.blue
        else:
            return None

    def set_colour(self, colour, value):
        if colour == "red":
            self.set_red(value)
        elif colour == "green":
            self.set_green(value)
        elif colour == "blue":
            self.set_blue(value)

    def set_red(self, value):
        self.red = value
        
    def set_green(self, value):
        self.green = value
        
    def set_blue(self, value):
        self.blue = value

    def is_possible(self):
        # Part 1 condition
        if self.red <= 12 and self.green <= 13 and self.blue <= 14:
            return True
        else:
            return False

class Game:
    def __init__(self, game_id):
        self.game_id = game_id
        self.cube_reveals = []

    def add_cube_reveal(self, cube_reveal):
        self.cube_reveals.append(cube_reveal)

    def is_possible(self):
        return all(cube_reveal.is_possible() for cube_reveal in self.cube_reveals)

    def min_cubes_required(self, colour):
        return max(cube_reveal.get_value_for_colour(colour) for cube_reveal in self.cube_reveals)

def parse_reveal_set(reveal_set_text):
    cube_reveal = CubeReveal()
    cube_reveal_texts = reveal_set_text.split(',')
    for cube_reveal_text in cube_reveal_texts:
        cube_reveal_parts = cube_reveal_text.strip().split(' ')
        count = int(cube_reveal_parts[0])
        colour = cube_reveal_parts[1]
        cube_reveal.set_colour(colour, count)
    return cube_reveal

def parse_input_line(input_line):
    parts = input_line.split(':')
    game = Game(int(parts[0].split(' ')[1]))
    reveal_set_texts = parts[1].split(';')
    for reveal_set_text in reveal_set_texts:
        game.add_cube_reveal(parse_reveal_set(reveal_set_text))
    return game

def get_power_value(game):
    red_required = game.min_cubes_required("red")
    green_required = game.min_cubes_required("green")
    blue_required = game.min_cubes_required("blue")
    return red_required * green_required * blue_required


puzzle_input = load_multi_line_input_as_string_list()
game_ids_sum = 0
game_power_sum = 0
for input_line in puzzle_input:
    game = parse_input_line(input_line)
    if game.is_possible():
        game_ids_sum += game.game_id
    game_power_sum += get_power_value(game)

print("Part 1: " + str(game_ids_sum))
print("Part 2: " + str(game_power_sum))
