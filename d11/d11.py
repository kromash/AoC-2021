import numpy as np


def read_input(filename):
    input = []
    with open(filename) as f:
        for line in f.readlines():
            input.append([int(c) for c in line.strip()])

    return np.array(input)


def build_energy(input):
    flashes = 0
    input += 1

    to_flash = []
    for i, line in enumerate(input):
        for j, e in enumerate(line):
            if e > 9:
                to_flash.append((i, j))
    flashed = set()
    while to_flash:
        i, j = to_flash.pop(0)

        if (i, j) in flashed:
            continue

        input[i, j] = 0
        for n in range(i - 1, i + 2):
            for m in range(j - 1, j + 2):
                if n == i and j == m:
                    continue
                if 0 <= n < input.shape[0] and 0 <= m < input.shape[1]:
                    if (n, m) in flashed:
                        continue
                    input[n, m] += 1
                    if input[n, m] > 9:
                        to_flash.append((n, m))

        flashes += 1
        flashed.add((i, j))
        print(i, j)

    return len(flashed)


def part_one(input):
    result = 0
    for i in range(100):
        result += build_energy(input)

    print(f'part one answer: {result}')


def part_two(input):
    result = 0
    squid_count = input.shape[0] * input.shape[1]
    for i in range(400):
        flashes = build_energy(input)
        if flashes == squid_count:
            result = i + 1
            break

    print(f'part one answer: {result}')


if __name__ == '__main__':
    input = read_input('d11.txt')
    # part_one(input)
    part_two(input)
