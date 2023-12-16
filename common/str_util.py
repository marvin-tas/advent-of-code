import re

def list_as_string_repr(l):
    return "[" + ", ".join(str(e) for e in l) + "]"

def remove_chars_from_string(s, chars):
    new_text = s
    for c in chars:
        new_text = new_text.replace(c, "")
    return new_text

def split_string_by_multiple_substrings(s, substrings):
    return re.split(s, "|".join(substrings))
