import numba

from utils.timeit import timing


def read_input(filename):
    input = []
    with open(filename) as f:
        for line in f.readlines():
            sections = line.strip().split('|')
            digits = [d.strip() for d in sections[0].strip().split(' ')]
            res = [d.strip() for d in sections[1].strip().split(' ')]
            input.append((digits, res))
    return input


def part_one(input):
    result = 0
    for digits, res in input:

        print(res)
        for d in res:
            if len(d) in [2, 3, 4, 7]:
                result += 1
    print(f'part one answer: {result}')


def solve(digits, res):
    print(digits, res)

    dig_by_seg = []
    for i in range(8):
        dig_by_seg.append([])
    for digit in digits:
        segments = frozenset(digit)

        dig_by_seg[len(segments)].append(segments)

    one = dig_by_seg[2][0]
    sev = dig_by_seg[3][0]
    eig = dig_by_seg[7][0]

    values = {}
    values[one] = 1
    values[sev] = 7
    values[eig] = 8
    values[dig_by_seg[4][0]] = 4

    t_f = {}
    t_f['d'] = (list(sev - one)[0])
    for five_seg in dig_by_seg[5]:
        if len(dig_by_seg[2][0] - five_seg) == 0:
            values[five_seg] = 3
        elif len(dig_by_seg[4][0] | five_seg) == 7:
            values[five_seg] = 2
        elif len(dig_by_seg[4][0] | five_seg) == 6:
            values[five_seg] = 5
    for six_seg in dig_by_seg[6]:
        if len(dig_by_seg[2][0] - six_seg) == 1:
            values[six_seg] = 6
        elif len(dig_by_seg[4][0] | six_seg) == 7:
            values[six_seg] = 0
        elif len(dig_by_seg[4][0] | six_seg) == 6:
            values[six_seg] = 9

    return int(''.join([str(values[frozenset(d)]) for d in res]))


@timing
def part_two(input):
    result = 0

    for digits, res in input:
        result += solve(digits, res)

    print(f'part two answer: {result}')


if __name__ == '__main__':
    input = read_input('d8.txt')
    # part_one(input)
    part_two(input)
