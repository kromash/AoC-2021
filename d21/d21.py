from copy import copy
from itertools import product
from math import floor

import numpy


def wrap_1_10(i):
    return i - 10 * floor((i - 1) / 10)


def get_roll(rolls):
    return rolls - 1000 * floor((rolls - 1) / 1000)


def dirac_one(start_1, start_2):
    rolls_num = 0
    pos_1 = start_1
    pos_2 = start_2
    score_1 = 0
    score_2 = 0
    while score_1 < 1000 and score_2 < 1000:
        roll_3 = 0
        for i in range(0, 3):
            rolls_num += 1
            roll_3 += get_roll(rolls_num)
        pos_1 = wrap_1_10(pos_1 + roll_3)
        score_1 += pos_1
        if score_1 >= 1000:
            break
        roll_3 = 0
        for i in range(0, 3):
            rolls_num += 1
            roll_3 += get_roll(rolls_num)
        pos_2 = wrap_1_10(pos_2 + roll_3)

        score_2 += pos_2

    print(score_1, score_2, rolls_num)
    print(f'part one answer: {score_2 * rolls_num}')


POSSIBLE_ROLLS = list(product(*[list(range(1, 4)) for _ in range(0, 3)]))


def dirac_move(start_position, roll):
    return wrap_1_10(start_position + sum(roll))


def game_recursive(players_position: tuple, points_to_score: tuple, winning_cheatsheet, current_player=0):
    if winning_cheatsheet[players_position[0]][players_position[1]][points_to_score[0]][points_to_score[1]][
        current_player].any():
        return winning_cheatsheet[players_position[0]][players_position[1]][points_to_score[0]][points_to_score[1]][
            current_player]
    wins = [0, 0]
    if points_to_score[current_player] <= 0:
        return wins

    next_player = (current_player + 1) % 2
    for roll in POSSIBLE_ROLLS:
        players_changed = list(copy(players_position))
        players_changed[current_player] = dirac_move(players_position[current_player], roll)
        scored = [0, 0]
        scored[current_player] += players_changed[current_player]

        if scored[current_player] >= points_to_score[current_player]:
            wins[current_player] += 1
        else:
            recursive_wins = game_recursive(tuple(players_changed), numpy.subtract(points_to_score, scored),
                                            winning_cheatsheet, next_player)
            wins = numpy.add(wins, recursive_wins)
    winning_cheatsheet[players_position[0]][players_position[1]][points_to_score[0]][points_to_score[1]][
        current_player] = wins
    return wins


def dirac_two(start_1, start_2, winning_score):
    winning_cheatsheet = numpy.zeros([11, 11, winning_score + 1, winning_score + 1, 2, 2])

    result = game_recursive(tuple([start_1, start_2]), tuple([winning_score, winning_score]), winning_cheatsheet)
    print(f'part two answer: {int(max(result))}')


if __name__ == '__main__':
    example_input = (4, 8)
    task_input = (9, 3)

    dirac_one(*example_input)
    dirac_one(*task_input)
    dirac_two(*task_input, 21)
