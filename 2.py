
DATAFILE = './data/2.txt'

# R/P/S scores
score_scales = {
    'R': 1,
    'P': 2,
    'S': 3
}

# map into RPS for sanity
canonical_map = {
    'A': 'R', 'B': 'P', 'C': 'S',
    'X': 'R', 'Y': 'P', 'Z': 'S'
}

part_two_map = {
    'X': 'L', 'Y': 'D', 'Z': 'W'
}

# Does left/first player win/lose or draw
score_map = {
    'RR': 3, 'RP': 0, 'RS': 6,
    'PR': 6, 'PP': 3, 'PS': 0,
    'SR': 0, 'SP': 6, 'SS': 3
}

# Throw map - for part two. Map their play and my goal into a score for that game.
throw_map = {
    'RW': 8, 'RL': 3, 'RD': 4,
    'PW': 9, 'PL': 1, 'PD': 5,
    'SW': 7, 'SL': 2, 'SD': 6

}


def score_game(me, opponent):
    me_c = canonical_map[me]
    them_c = canonical_map[opponent]
    game_score = score_map[me_c + them_c] + score_scales[me_c]
    # print(f"{me_c} vs {them_c} = {game_score}")
    return game_score


def test_scoring():
    them = 'ABC'
    me = 'YXZ'
    total_score = 0
    for i in range(len(them)):
        total_score += score_game(me[i], them[i])
    assert(total_score == 15)


def run_games():
    game_lines = open(DATAFILE, 'r').readlines()
    total = 0
    for game in game_lines:
        gestures = game.strip().split(' ')
        them_c = gestures[0]
        me_c = gestures[1]
        total += score_game(me_c, them_c)

    print(f'Total is {total} for {len(game_lines)} games')


# Part Two - throw the games, compute the score.
def run_thrown_games():
    game_lines = open(DATAFILE, 'r').readlines()
    total = 0
    for game in game_lines:
        gestures = game.strip().split(' ')
        them_c = canonical_map[gestures[0]]
        me_c = part_two_map[gestures[1]]
        total += throw_map[them_c + me_c]

    print(f'Total is {total} for thrown {len(game_lines)} games')


if __name__ == '__main__':
    test_scoring()
    run_games()
    run_thrown_games()