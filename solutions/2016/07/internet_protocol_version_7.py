import sys
sys.path.append('../../../common')
from parser import *

def contains_abba_substring(s):
    s_array = list(s)
    for i in range(len(s_array) - 3):
        if s_array[i] == s_array[i + 1]:
            continue
        if s_array[i] == s_array[i + 3] and s_array[i + 1] == s_array[i + 2]:
            return True
    return False

def line_supports_tls(pi_line):
    inside_bracket_strings = pi_line[1::2]
    outside_bracket_strings = pi_line[0::2]

    for s in inside_bracket_strings:
        if contains_abba_substring(s):
            return False
    for s in outside_bracket_strings:
        if contains_abba_substring(s):
            return True
    return False
    
def get_all_aba_substrings(s):
    s_array = list(s)
    aba_substrings = []
    for i in range(len(s_array) - 2):
        if s_array[i] == s_array[i + 1]:
            continue
        if s_array[i] == s_array[i + 2]:
            aba_substrings.append("".join(s_array[i:i+3]))
    return aba_substrings

def is_aba_and_bab(s_aba, s_bab):
    s_aba_array = list(s_aba)
    s_bab_array = list(s_bab)
    return s_aba_array[0] == s_bab_array[1] and s_aba_array[1] == s_bab_array[0]

def line_supports_ssl(pi_line):
    inside_bracket_strings = pi_line[1::2]
    outside_bracket_strings = pi_line[0::2]

    inside_bracket_aba_substrings = []
    outside_bracket_aba_substrings = []

    for s in inside_bracket_strings:
        inside_bracket_aba_substrings.extend(get_all_aba_substrings(s))
    for s in outside_bracket_strings:
        outside_bracket_aba_substrings.extend(get_all_aba_substrings(s))

    for s1 in inside_bracket_aba_substrings:
        for s2 in outside_bracket_aba_substrings:
            if is_aba_and_bab(s1, s2):
                return True
    return False

puzzle_input = load_multi_line_input(['\n'], ['[', ']'])

n_supports_tls = 0
n_supports_ssl = 0
for pi in puzzle_input:
    if line_supports_tls(pi):
        n_supports_tls += 1
    if line_supports_ssl(pi):
        n_supports_ssl += 1
        
print("Part 1: " + str(n_supports_tls))

print("Part 2: " + str(n_supports_ssl))
