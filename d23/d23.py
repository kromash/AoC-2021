import copy

import numpy as np
from numba import jit

from utils.timeit import timing


def read_input(filename, n=2):
    input = []
    with open(filename) as f:
        lines = f.readlines()

    for j in range(n):
        input.append([ord(lines[j + 2][3 + i * 2]) - ord('A') for i in range(0, 4)] + [-1] * 7)
    return input


@jit(nopython=True)
def _convert_from_hole_index(hole_index):
    return 2 + hole_index * 2


@jit(nopython=True)
def move(input, start, end):
    c = input[start]
    input[end] = c
    input[start] = -1

    x1 = start[1] if start[0] == 0 else _convert_from_hole_index(start[1])
    x2 = end[1] if end[0] == 0 else _convert_from_hole_index(end[1])
    cost = (abs(end[0] - start[0]) + abs(x2 - x1)) * (10 ** c)
    could_be_solved = (end[0] == 1) and (c == end[1])
    return cost, could_be_solved


@jit(nopython=True)
def _int_to_char(i):
    return chr(i + ord('A'))


def print_board(input):
    print(f"#{''.join([_int_to_char(c) if c != -1 else '.' for c in input[0]])}#")
    for i in range(1, input.shape[0]):
        print(f'###{"#".join([_int_to_char(c) if c != -1 else "." for c in input[i][0:4]])}###')
    print()


@jit(nopython=True)
def get_possible_moves(input):
    possible_moves = []
    h = input.shape[0]

    for i, value in enumerate(input[0]):
        if value != -1:
            j = _convert_from_hole_index(value)
            if j > i:
                s = i + 1
                e = j + 1
            else:
                s = j
                e = i

            if len([el for el in input[0][s:e] if el != -1]) > 0:
                continue
            for k in range(h - 1, 0, -1):
                if input[k, value] != value:
                    if input[k, value] == -1:
                        return [((0, i), (k, value))]
                    else:
                        break

    for i in range(4):
        j = 1

        hori_line = [input[k, i] == -1 or input[k, i] == i for k in range(1, h)]
        if sum(hori_line) == h - 1:
            continue
        while j < h:
            value = input[j, i]
            if value != -1:

                k = _convert_from_hole_index(i)
                d = k - 1
                while d >= 0 and input[0, d] == -1:
                    if d not in [2, 4, 6, 8]:
                        possible_moves.append(((j, i), (0, d)))
                    d -= 1

                d = k + 1
                while d < 11 and input[0, d] == -1:
                    if d not in [2, 4, 6, 8]:
                        possible_moves.append(((j, i), (0, d)))
                    d += 1

                break
            j += 1

    return possible_moves


@jit(nopython=True)
def check_solved(input):
    for j in range(1, 3):
        for i, value in enumerate(input[j][0:4]):
            if value != i:
                return False
    return True


min_cost = 100000
initial_input = None
moves = []


def solve_one(input, cost=0, could_be_solved=False):
    # print_board(input)
    global min_cost
    if cost > min_cost:
        return
    if could_be_solved and check_solved(input):
        global initial_input
        if cost < min_cost:
            _initial_input = copy.deepcopy(initial_input)
            print(f'SOLVED: {cost}')
            # print_board(input)
            min_cost = cost
            for _move in moves:
                move(_initial_input, _move[0], _move[1])
                print_board(_initial_input)
            print(f'SOLVED: {cost}')
    for fr, to in get_possible_moves(input):
        moves.append((fr, to))
        _c, cbs = move(input, fr, to)
        cost += _c
        solve_one(input, cost, cbs)
        move(input, to, fr)
        cost -= _c
        moves.pop(len(moves) - 1)


@timing
def part_one(input):
    global initial_input
    upper_space = [-1] * 11
    input = np.array([upper_space] + input)
    initial_input = copy.deepcopy(input)
    print_board(input)
    solve_one(input)


def part_two(input):
    global initial_input
    upper_space = [-1] * 11
    input = np.array([upper_space] + input)
    initial_input = copy.deepcopy(input)
    print_board(input)
    solve_one(input)


if __name__ == '__main__':
    # input = read_input('d23.txt')
    # part_one(input)

    input = read_input('d23_2.txt', n=4)
    part_two(input)
