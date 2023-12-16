import sys
sys.path.append('../../../common')
from parser import *

digit_texts = {
    "one": '1',
    "two": '2',
    "three": '3',
    "four": '4',
    "five": '5',
    "six": '6',
    "seven": '7',
    "eight": '8',
    "nine": '9'
}

# Problem #1 (part 2): eightwo -> should be 8wo and not eigh2
# Unfortunately we cannot do the replacements topologically as we have a cycle of potential embeddedness: ..twoneightwoneight..
# Also as discovered later, we would have to reverse the topological ordering as well to prioritise the last possible digit
#   i.e. twone would have "two" as the first digit but "one" as the last


def get_calibration_code_1(input_line):
    numeric_values = [c for c in list(input_line) if c.isnumeric()]
    return int(numeric_values[0] + numeric_values[-1])

def get_calibration_code_2(input_line):
    first_digit = None
    last_digit = None
    char_index = 0
    while (char_index < len(input_line)):
        current_digit = None
        current_character = input_line[char_index]
        if current_character.isnumeric():
            current_digit = current_character
        else:
            for digit_text in digit_texts:
                digit_text_length = len(digit_text)
                if len(input_line) < char_index + digit_text_length:
                    continue
                if input_line[char_index:char_index + digit_text_length] == digit_text:
                    current_digit = digit_texts[digit_text]
                    break
        if current_digit is not None:
            if first_digit is None:
                first_digit = current_digit
            last_digit = current_digit
        char_index += 1
    return int(first_digit + last_digit)
    

puzzle_input_lines = load_multi_line_input_as_string_list()
calibration_code_sum_1 = 0
calibration_code_sum_2 = 0

for puzzle_input_line in puzzle_input_lines:
    calibration_code_sum_1 += get_calibration_code_1(puzzle_input_line)
    calibration_code_sum_2 += get_calibration_code_2(puzzle_input_line)


print("Part 1: " + str(calibration_code_sum_1))
print("Part 2: " + str(calibration_code_sum_2))
