import numpy as numpy
import re


def read_input(filename):
    reg = '([0-9]+),([0-9]+) -> ([0-9]+),([0-9]+)'
    with open(filename) as f:
        lines = [re.search(reg, line.strip()) for line in f.readlines()]
        return [[int(line.group(i)) for i in range(1, 5)] for line in lines]


def print_board(board):
    for line in board:
        print(''.join([str(i) for i in line]))


def add_straight_lines(board, lines):
    crosses = 0
    for line in lines:
        x = None
        y = None
        if line[0] == line[2]:
            x = line[0]
        elif line[1] == line[3]:
            y = line[1]

        if x:
            y_start = min(line[1], line[3])
            y_end = max(line[1], line[3])
            for i in range(y_start, y_end + 1):
                board[i][x] += 1
                if board[i][x] == 2:
                    crosses += 1

        if y:
            x_start = min(line[0], line[2])
            x_end = max(line[0], line[2])
            for i in range(x_start, x_end + 1):
                # if board[y][i] == 1:
                #     crosses += 1
                board[y][i] += 1
                if board[y][i] == 2:
                    crosses += 1
    return crosses


def venture_one(lines):
    crosses = 0
    max_cord = max([item for sublist in lines for item in sublist])
    board = [None] * (max_cord + 1)
    for i in range(0, max_cord + 1):
        board[i] = [0] * (max_cord + 1)

    crosses += add_straight_lines(board, lines)
    print(f'crosses: {crosses}')


def add_diag_lines(board, lines):
    crosses = 0

    for line in lines:
        x1 = line[0]
        y1 = line[1]
        x2 = line[2]
        y2 = line[3]
        if x1 != x2 and y1 != y2:
            x = x1
            y = y1
            x_diff = numpy.sign(x2 - x1)
            y_diff = numpy.sign(y2 - y1)
            while x != x2 and y != y2:
                board[y][x] += 1
                if board[y][x] == 2:
                    crosses += 1
                x += x_diff
                y += y_diff
            board[y][x] += 1
            if board[y][x] == 2:
                crosses += 1

    return crosses


def venture_two(lines):
    crosses = 0
    max_cord = max([item for sublist in lines for item in sublist])
    board = [None] * (max_cord + 1)
    for i in range(0, max_cord + 1):
        board[i] = [0] * (max_cord + 1)

    crosses += add_straight_lines(board, lines)
    crosses += add_diag_lines(board, lines)
    print(f'crosses: {crosses}')


if __name__ == '__main__':
    venture_one(read_input('d5.txt'))
    venture_two(read_input('d5.txt'))
