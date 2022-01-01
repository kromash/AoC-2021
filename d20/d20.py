from itertools import product

import numpy as np


def print_board(matrix):
    for line in matrix:
        print(''.join(['#' if e == 1 else '.' for e in line]))


def read_input(filename):
    with open(filename) as f:
        alg = [0 if c == '.' else 1 for c in f.readline().strip()]
        matrix = []
        f.readline()
        for line in f.readlines():
            matrix.append([0 if c == '.' else 1 for c in line.strip()])
    return np.array(alg, dtype=int), np.array(matrix, dtype=int)


# @jit(nopython=True)
def expand(alg, matrix, nodata=0):
    # matrix = deepcopy(matrix)
    new_matrix = np.zeros((matrix.shape[1] + 2, matrix.shape[0] + 2), dtype=int)
    for j in range(-1, matrix.shape[1] + 1):
        for i in range(-1, matrix.shape[0] + 1):
            a = ''.join(
                np.array(get_with_defaults(matrix, range(i - 1, i + 2), range(j - 1, j + 2), nodata=nodata), dtype=str))
            # print(a)
            index = int(a, 2)
            # print(alg[index])
            new_matrix[j + 1][i + 1] = alg[index]
    # break

    return new_matrix


# @jit(nopython=True)
def get_with_defaults(a, xx, yy, nodata=0):
    p = list(product(yy, xx))
    # print(list(xx))
    xx = [x[1] for x in p]
    yy = [x[0] for x in p]
    # print('x', xx)
    # print('y', yy)
    # get values from a, clipping the index values to valid ranges
    res = a[np.clip(yy, 0, a.shape[0] - 1), np.clip(xx, 0, a.shape[1] - 1)]
    # compute a mask for both x and y, where all invalid index values are set to true
    myy = np.ma.masked_outside(yy, 0, a.shape[0] - 1).mask
    mxx = np.ma.masked_outside(xx, 0, a.shape[1] - 1).mask
    # replace all values in res with NODATA, where either the x or y index are invalid
    np.choose(myy + mxx, [res, nodata], out=res)
    return res


def part_one(alg, matrix):
    print(alg)
    print(matrix.shape, matrix.sum())
    print_board(matrix)
    print()
    print()
    matrix = expand(alg, matrix)
    print_board(matrix)
    print(matrix.shape, matrix.sum())
    print()
    print()
    matrix = expand(alg, matrix)
    print_board(matrix)
    print(matrix.shape, matrix.sum())
    result = matrix.sum()
    print(matrix.shape, result)

    print(f'part two answer: {result}')


def part_two(alg, matrix):
    for i in range(50):
        print(i)
        matrix = expand(alg, matrix, nodata=i % 2)
    result = matrix.sum()
    print(f'part two answer: {result}')


if __name__ == '__main__':
    # 5171 too low
    # 5652 too high
    # 6045 too high
    alg, matrix = read_input('d20.txt')
    part_two(alg, matrix)
    # part_two(input)
