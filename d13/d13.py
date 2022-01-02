import numpy as np


def read_input(filename):
    dots = []
    folds = []
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            if line == '':
                continue
            if 'x' in line:
                parts = line.split('=')
                folds.append(tuple(['x', int(parts[1])]))
                continue
            if 'y' in line:
                parts = line.split('=')
                folds.append(tuple(['y', int(parts[1])]))
                continue
            dots.append(tuple(int(i) for i in line.split(',')))
    return dots, folds


def fold_y(dots, fold_y):
    new_dots = set()

    for x, y in dots:
        if y < fold_y:
            new_dots.add(tuple([x, y]))
        if y > fold_y:
            new_dots.add(tuple([x, fold_y - (y - fold_y)]))
    return new_dots


def fold_x(dots, fold_x):
    new_dots = set()
    for x, y in dots:
        if x < fold_x:
            new_dots.add(tuple([x, y]))
        if x > fold_x:
            new_dots.add(tuple([fold_x - (x - fold_x), y]))
    return new_dots


def part_one(dots, folds):
    result = 0
    for fold in folds:
        if fold[0] == 'y':
            dots = fold_y(dots, fold[1])
        if fold[0] == 'x':
            dots = fold_x(dots, fold[1])
        break
    result = len(dots)
    print(f'part one answer: {result}')


def part_two(dots, folds):
    for fold in folds:
        if fold[0] == 'y':
            dots = fold_y(dots, fold[1])
        if fold[0] == 'x':
            dots = fold_x(dots, fold[1])

    max_x = max([x for x, y in dots])
    max_y = max([y for x, y in dots])
    paper = np.zeros((max_x + 1, max_y + 1), dtype=int)
    for dot in dots:
        paper[dot] = 1

    print('part two answer:')
    for line in np.transpose(paper):
        print(''.join(['#' if c else '.' for c in line]))


if __name__ == '__main__':
    dots, folds = read_input('d13.txt')

    part_one(dots, folds)
    part_two(dots, folds)
