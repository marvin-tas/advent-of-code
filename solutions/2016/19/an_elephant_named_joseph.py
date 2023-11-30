puzzle_input = 3017957

# Each round the evens will be eliminated and the next will have only the odds
# If the number is odd: The first is eliminated by the last of the previous round
# If the number is even: The first is not eliminated

# If there is 1 left, they win
# If there is 2 left, the first wins


# Question: How do we efficiently keep a record?
# Theres gotta be a clean way e.g. if the number is 2^x then it will always be the first?

def get_winner(players):
    n_players = len(players)
    if n_players == 1 or n_players == 2:
        return players[0]
    odd_players = players[::2]
    if n_players % 2 == 0:
        return get_winner(odd_players)
    else:
        return get_winner(odd_players[1:])

print("Part 1: " + str(get_winner(range(1, puzzle_input + 1))))
