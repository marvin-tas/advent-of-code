def load_multi_line_input_as_character_arrays():
    lines = read_input_file()
    contents = []
    for line in lines:
        contents.append([c for c in line.strip()])
    return contents

def load_multi_line_input(characters_to_remove, delimeters):
    lines = read_input_file()
    contents = []
    for line in lines:
        s = remove_characters_from_string(line, characters_to_remove)
        contents.append(split_string_by_delimeters(s, delimeters))
    return contents

def load_multi_line_input_separated_by_spaces():
    lines = read_input_file()
    contents = []
    for line in lines:
        contents.append(line.split())
    return contents


def load_single_line_input(characters_to_remove, delimeters):
    line = read_input_file()[0]
    s = remove_characters_from_string(line, characters_to_remove)
    return split_string_by_delimeters(s, delimeters)

def read_input_file():
    f = open('input.txt', 'r')
    contents = f.readlines()
    f.close()
    return contents

def remove_characters_from_string(s, characters_to_remove):
    for c in characters_to_remove:
        s = s.replace(c, '')
    return s

def split_string_by_delimeters(s, delimeters):
    strings_to_concat = [s]
    for delim in delimeters:
        new_substrings = []
        for partial_string in strings_to_concat:
            new_substrings.extend(partial_string.split(delim))
        strings_to_concat = new_substrings
    return strings_to_concat
