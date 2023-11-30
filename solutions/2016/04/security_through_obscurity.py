import sys
sys.path.append('../../../common')
from parser import *

puzzle_input = load_multi_line_input([']', '\n'],['-', '['])

def interpret_input_line(line):
    checksum = line[-1]
    sector_id = int(line[-2])
    room_name = "-".join(line[:-2])
    return room_name, sector_id, checksum

def verify_room(room_name, checksum):
    room_name_chars = list(remove_characters_from_string(room_name, ["-"]))
    char_set = set(room_name_chars)
    counts = {}
    for c in char_set:
        count = room_name_chars.count(c)
        if count in counts:
            counts[count].append(c)
        else:
            counts[count] = [c]
    expected_checksum = []
    for count_n in reversed(sorted(counts)):
        n_can_add = max(0, 5 - len(expected_checksum))
        next_to_add = sorted(counts[count_n])
        expected_checksum.extend(next_to_add[:min(n_can_add, len(next_to_add))])
    return "".join(expected_checksum) == checksum

def convert_lower_case_letter_to_alphabet_number(character):
    return ord(character) - 97

def convert_alphabet_number_to_lower_case_letter(number):
    return chr(ord('`')+number+1)


def shift_character(c, shift):
    original_alphabet_number = convert_lower_case_letter_to_alphabet_number(c)
    shifted_alphabet_number = (original_alphabet_number + shift) % 26
    return convert_alphabet_number_to_lower_case_letter(shifted_alphabet_number)

def decrypt_room_name(room_name, sector_id):
    words = room_name.split("-")
    new_words = []
    for word in words:
        new_word = ""
        for letter in word:
            new_word += shift_character(letter, sector_id)
        new_words.append(new_word)
    return " ".join(new_words)

total_sector_id = 0
north_pole_storage_sector_id = None
north_pole_storage_name = "northpole object storage"
for pi in puzzle_input:
    room_name, sector_id, checksum = interpret_input_line(pi)
    if (verify_room(room_name, checksum)):
        total_sector_id += sector_id
    if decrypt_room_name(room_name, sector_id) == north_pole_storage_name:
        north_pole_storage_sector_id = sector_id

print("Part 1: " + str(total_sector_id))
print("Part 2: " + str(north_pole_storage_sector_id))
