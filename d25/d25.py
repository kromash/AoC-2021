import numpy as np


def read_input(filename):
    input = []
    with open(filename) as f:
        for line in f.readlines():
            input.append([c for c in line.strip()])

    return np.array(input)


def part_one(input):
    result = 0
    h = input.shape[0]
    w = input.shape[1]
    right_move = set()
    down_move = set()
    for i, line in enumerate(input):
        for j, c in enumerate(line):
            if c == '>':
                right_move.add(tuple([i, j]))
            if c == 'v':
                down_move.add(tuple([i, j]))
    while right_move or down_move:
        result += 1
        new_right_move = set()
        new_down_move = set()
        to_right_move = []
        to_down_move = []
        for move in right_move:
            i = move[0]
            j = move[1]

            if input[i][(j + 1) % w] == '.':
                to_right_move.append([i, j])
                new_right_move.add(tuple([i, (j + 1) % w]))
                if input[(i + h - 1) % h][j] == 'v':
                    down_move.add(tuple([(i + h - 1) % h, j]))
                elif input[i][(j + w - 1) % w] == '>':
                    new_right_move.add(tuple([i, (j + w - 1) % w]))

        for i, j in to_right_move:
            input[i][j] = '.'
            input[i][(j + 1) % w] = '>'

        for move in down_move:
            i = move[0]
            j = move[1]
            if input[(i + 1) % h][j] == '.':
                to_down_move.append([i, j])
                new_down_move.add(tuple([(i + 1) % h, j]))
                if input[i][(j + w - 1) % w] == '>':
                    new_right_move.add(tuple([i, (j + w - 1) % w]))
                elif input[(i + h - 1) % h][j] == 'v':
                    new_down_move.add(tuple([(i + h - 1) % h, j]))
        for i, j in to_down_move:
            input[i][j] = '.'
            input[(i + 1) % h][j] = 'v'

        right_move = new_right_move
        down_move = new_down_move
        print(result, len(right_move), len(down_move))
    print(f'part one answer: {result}')


if __name__ == '__main__':
    input = read_input('d25.txt')
    part_one(input)
