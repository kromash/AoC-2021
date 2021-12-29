def read_input(filename):
    input = []
    with open(filename) as f:
        for line in f.readlines():
            input.append(line.strip())

    return input


def part_one(input):
    result = 0
    print(f'part one answer: {result}')


def part_two(input):
    result = 0
    print(f'part two answer: {result}')


if __name__ == '__main__':
    input = read_input('d9_ex.txt')
    part_one(input)
    # part_two(input)
