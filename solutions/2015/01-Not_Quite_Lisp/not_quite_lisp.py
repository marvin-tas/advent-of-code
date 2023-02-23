def get_puzzle_input():
    f = open('input.txt', 'r')
    contents = f.readlines()
    f.close()
    return contents

def process_direction(direction):
    match direction:
        case '(':
            return 1
        case ')':
            return -1
        case _:
            raise Exception("Cannot process direction:" + str(direction))

def get_final_floor(directions):
    return sum([process_direction(direction) for direction in directions])

def get_num_steps_to_floor(directions, target_floor):
    current_floor = 0
    n = 0
    for direction in directions:
        if current_floor is target_floor:
            return n
        n += 1
        current_floor += process_direction(direction)
    return None

directions = get_puzzle_input()[0]

# Part 1
print("Part 1:" + str(get_final_floor(directions)))

# Part 2
print("Part 2:" + str(get_num_steps_to_floor(directions, -1)))
        
