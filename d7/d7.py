import numpy


def read_input(filename):
    with open(filename) as f:
        return [int(n) for n in f.readline().strip().split(',')]


def part_one(input):
    max_x = max(input)
    dists = []
    for j in input:
        dists.append([abs(i - j) for i in range(0, max_x + 1)])
    dists = numpy.array(dists)
    result = numpy.min(numpy.sum(dists, axis=0))

    print(f'part one answer: {result}')


def _move_sum(dist):
    return (dist) * (dist + 1) / 2


def part_two(input):
    max_x = max(input)
    dists = []
    for j in input:
        dists.append([_move_sum(abs(i - j)) for i in range(0, max_x + 1)])

    dists = numpy.array(dists)
    result = numpy.min(numpy.sum(dists, axis=0))

    print(f'part two answer: {result}')


if __name__ == '__main__':
    input = read_input('d7.txt')
    part_one(input)
    part_two(input)
