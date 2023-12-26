import sys
sys.path.append('../../../common')
from parser import *

class Present:

    def __init__(self, l, w, h):
        self.l = l
        self.w = w
        self.h = h

    def get_required_wrapping_paper(self):
        surface_area = 2*self.l*self.w + 2*self.w*self.h + 2*self.h*self.l
        sides = sorted([self.l, self.w, self.h])
        slack = sides[0]*sides[1]
        return 2*self.l*self.w + 2*self.w*self.h + 2*self.h*self.l + slack

    def get_required_ribbon(self):
        sides = sorted([self.l, self.w, self.h])
        return 2*sides[0] + 2*sides[1] + self.get_volume()

    def get_volume(self):
        return self.l * self.w * self.h
        

puzzle_input = load_multi_line_input([], ['x'])

presents = [Present(int(input_line[0]), int(input_line[1]), int(input_line[2])) for input_line in puzzle_input]

total_wrapping_paper = sum([present.get_required_wrapping_paper() for present in presents])
total_ribbon = sum([present.get_required_ribbon() for present in presents])

print("Part 1: " + str(total_wrapping_paper))
print("Part 2: " + str(total_ribbon))
