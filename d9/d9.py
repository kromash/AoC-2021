import numpy as np


def read_input(filename):
    input = []
    with open(filename) as f:
        for line in f.readlines():
            input.append([int(d) for d in line.strip()])

    return np.array(input)


def _get_lowest_points(input):
    h = input.shape[0]
    w = input.shape[1]
    results = []
    for i, line in enumerate(input):
        for j, e in enumerate(line):
            adjacent = []
            if i > 0:
                adjacent.append(input[i - 1, j])
            if i < h - 1:
                adjacent.append(input[i + 1, j])
            if j > 0:
                adjacent.append(input[i, j - 1])
            if j < w - 1:
                adjacent.append(input[i, j + 1])
            if e < min(adjacent):
                results.append((i, j))
    return results


def part_one(input):
    lowest_points = _get_lowest_points(input)

    result = sum([input[i][j] + 1 for i, j in lowest_points])
    print(f'part one answer: {result}')


def part_two(input):
    h = input.shape[0]
    w = input.shape[1]
    lowest_points = _get_lowest_points(input)
    areas = []
    for point in lowest_points:
        q = [point]
        visited = []

        while q:
            i, j = q.pop()
            if (i, j) in visited or input[i, j] == 9:
                continue
            visited.append((i, j))

            if i > 0:
                q.append((i - 1, j))
            if i < h - 1:
                q.append((i + 1, j))
            if j > 0:
                q.append((i, j - 1))
            if j < w - 1:
                q.append((i, j + 1))
        areas.append(len(visited))

    list.sort(areas, reverse=True)
    print(areas[0:3])
    result = 1
    for area in areas[0:3]:
        result *= area
    print(f'part two answer: {result}')


if __name__ == '__main__':
    input = read_input('d9.txt')
    # part_one(input)
    part_two(input)
