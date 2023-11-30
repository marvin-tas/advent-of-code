import sys
sys.path.append('../../../common')
from parser import *


class Pixel:
    def __init__(self):
        self.on = False

    def is_on(self):
        return self.on

    def turn_on(self):
        self.on = True

    def turn_off(self):
        self.on = False

    def set_on(self, is_on):
        self.on = is_on

    def toggle(self):
        self.on = not self.on

    def __str__(self):
        return "#" if self.on else "."

class PixelMatrix:

    def __init__(self, n_rows, n_cols):
        self.pixels = []
        self.n_rows = n_rows
        self.n_cols = n_cols
        for r in range(n_rows):
            self.pixels.append([Pixel() for c in range(n_cols)])

    def rotate_pixel_row(self, row_n, rotation):
        self.rotate_pixel_array(self.get_pixel_row(row_n), rotation)

    def rotate_pixel_col(self, col_n, rotation):
        self.rotate_pixel_array(self.get_pixel_col(col_n), rotation)

    @staticmethod
    def rotate_pixel_array(pixel_array, rotation):
        array_len = len(pixel_array)
        # Get copy of the current statuses before modification
        current_statuses = [pixel.is_on() for pixel in pixel_array]
        for i in range(array_len):
            is_currently_on = current_statuses[i]
            pixel = pixel_array[(i + rotation) % array_len]
            pixel.set_on(is_currently_on)

    def turn_on_upper_left_sub_matrix(self, n_sub_rows, n_sub_cols):
        sub_matrix = self.get_origin_sub_matrix(n_sub_rows, n_sub_cols)
        for pixel_row in sub_matrix:
            for pixel in pixel_row:
                pixel.turn_on()

    def get_pixel_row(self, row_n):
        return self.pixels[row_n]

    def get_pixel_col(self, col_n):
        pixels = []
        for r in range(self.n_rows):
            pixels.append(self.pixels[r][col_n])
        return pixels

    def get_origin_sub_matrix(self, n_sub_rows, n_sub_cols):
        sub_matrix = []
        for r in range(n_sub_rows):
            sub_matrix.append(self.pixels[r][:n_sub_cols])
        return sub_matrix

    def get_number_of_pixels_on(self):
        n_pixels_on = 0
        for pixel_row in self.pixels:
            for pixel in pixel_row:
                if pixel.is_on():
                    n_pixels_on += 1
        return n_pixels_on

    def __str__(self):
        s = ""
        for r in range(self.n_rows):
            s += ("".join([str(pixel) for pixel in self.pixels[r]]) + "\n")
        return s

def process_rect_command(args, pixel_matrix):
    values = args[0].split('x')
    n_rect_cols = int(values[0])
    n_rect_rows = int(values[1])
    pixel_matrix.turn_on_upper_left_sub_matrix(n_rect_rows, n_rect_cols)
    
def process_rotate_command(args, pixel_matrix):
    n_row_or_col = int(args[1].split('=')[1])
    rotation = int(args[3])
    if args[0] == "row":
        pixel_matrix.rotate_pixel_row(n_row_or_col, rotation)
    elif args[0] == "column":
        pixel_matrix.rotate_pixel_col(n_row_or_col, rotation)
    else:
        raise("Invalid rotation parameter")

def process_input_line(line, pixel_matrix):
    command = line[0]
    args = line[1:]
    if command == "rect":
        process_rect_command(args, pixel_matrix)
    elif command == "rotate":
        process_rotate_command(args, pixel_matrix)
    else:
        raise("Line does not start with a valid command")

puzzle_input = load_multi_line_input(["\n"], [" "])
pm = PixelMatrix(6, 50)

for pi in puzzle_input:
    process_input_line(pi, pm)

print("Part 1: " + str(pm.get_number_of_pixels_on()))

print("Part 2: \n" + str(pm))
