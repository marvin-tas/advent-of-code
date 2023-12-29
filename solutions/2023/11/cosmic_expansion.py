import sys
sys.path.append('../../../common')
from parser import *
from grid import *

class Universe:
    def __init__(self, galaxies):
        # Point of reference is (0,0) so that all positions are in non-negative coords
        self.galaxies = galaxies
        galaxy_positions = [galaxy.position for galaxy in galaxies]
        self.width = max([position.x for position in galaxy_positions])
        self.height = max([position.y for position in galaxy_positions])

    def expand(self, amount):
        vertical_expansions = []
        horizontal_expansions = []
        # Expanding occurs from reference 0,0
        for y in range(self.height):
            if y not in [galaxy.position.y for galaxy in self.galaxies]:
                vertical_expansions.append(y)
        for x in range(self.width):
            if x not in [galaxy.position.x for galaxy in self.galaxies]:
                horizontal_expansions.append(x)

        for galaxy in self.galaxies:
            pos = galaxy.position
            dy = sum([pos.y > y for y in vertical_expansions])
            dx = sum([pos.x > x for x in horizontal_expansions])
            displacement = GridDisplacement(amount * dx, amount * dy)
            galaxy.shift_position(displacement)

        self.height += amount * len(vertical_expansions)
        self.width += amount * len(horizontal_expansions)

    def get_sum_of_distances_between_all_galaxy_pairs(self):
        total = 0
        for g1 in range(len(self.galaxies) - 1):
            for g2 in range(g1 + 1, len(self.galaxies)):
                galaxy1 = self.galaxies[g1]
                galaxy2 = self.galaxies[g2]
                total += galaxy1.distance_to_other(galaxy2)
        return total


class Galaxy:
    def __init__(self, position):
        self.position = position

    def __hash__(self):
        return hash(self.position)

    def __eq__(self, other):
        return self.position == other.position

    def __str__(self):
        return "#@" + str(self.position)

    def __repr__(self):
        return str(self)

    def shift_position(self, displacement):
        self.position = self.position.position_at_displacement(displacement)

    def distance_to_other(self, other):
        return self.position.manhattan_distance_from_other(other.position)

class GalaxyImage:
    def __init__(self, image_text):
        self.galaxy_positions = []
        self.height = len(image_text)
        self.width = len(image_text[0])
        for r in range(self.height):
            current_image_row = image_text[r]
            for c in range(self.width):
                if current_image_row[c] == '#':
                    self.galaxy_positions.append(GridPosition(c, r))


def parse_puzzle_input(puzzle_input):
    # Reverse the lines so positive y is up
    return GalaxyImage(puzzle_input[::-1])

galaxy_image = parse_puzzle_input(load_multi_line_input_as_character_arrays())
universe1 = Universe([Galaxy(position) for position in galaxy_image.galaxy_positions])
universe2 = Universe([Galaxy(position) for position in galaxy_image.galaxy_positions])

universe1.expand(1)
universe2.expand(999999) # -1 since thats how many extra there is

print("Part 1: " + str(universe1.get_sum_of_distances_between_all_galaxy_pairs()))
print("Part 2: " + str(universe2.get_sum_of_distances_between_all_galaxy_pairs()))
