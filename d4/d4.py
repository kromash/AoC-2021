import numpy
import numpy as np
from numpy import ma


def read_input(filename):
    with open(filename) as f:
        numbers = [int(i) for i in f.readline().strip().split(',')]

        boards = []
        for line in f.readlines():
            if not line.strip():
                continue
            boards.append([int(i) for i in line.strip().split(' ') if i])
        boards = numpy.array(boards)
        return numbers, np.array(np.split(boards, len(boards)/5))

def bingo_one(numbers, boards, which_win = 1):
    arr = np.zeros([len(boards), 2, 5])
    won = set()
    masks = np.zeros([len(boards), 5, 5])
    for number in numbers:
        coords = list(zip(*np.where(boards == number)))

        for board, x, y in coords:
            arr[board][0][x] += 1
            arr[board][1][y] += 1
            masks[board][x][y] = 1
            if arr[board][0][x] == 5 or arr[board][1][y] == 5:
                won.add(board)
                if len(won) == which_win:
                    ma_array = ma.array(boards[board], mask=masks[board])
                    print(ma_array.sum(), number, ma_array.sum() * number)
                    return

if __name__ == '__main__':
    numbers, boards = read_input('d4.txt')

    bingo_one(numbers, boards)
    bingo_one(numbers, boards, len(boards))
