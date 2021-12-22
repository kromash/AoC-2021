from copy import copy


def binary_diagnostic_one(filename):
    with open(filename) as f:
        lines = []
        for line in f.readlines():
            lines.append(line.strip())

        width = len(lines[0])
        ones = [0] * width
        for line in lines:
            for i in range(0, width):
                ones[i] += int(line[i])
        print(ones)
        rows = len(lines)
        gamma = int(''.join([str(int(row > rows / 2)) for row in ones]), 2)
        epsilon = int(''.join([str(int(row < rows / 2)) for row in ones]), 2)
        print(gamma, epsilon, gamma * epsilon)


def keep_most_common(lines, bit):
    ones = [line[bit] == '1' for line in lines]
    most_common = '1' if sum(ones) >= len(lines) / 2 else '0'
    print(most_common)
    return [line for line in lines if line[bit] == most_common]


def keep_least_common(lines, bit):
    ones = [line[bit] == '1' for line in lines]
    most_common = '1' if sum(ones) < len(lines) / 2 else '0'
    print(most_common)
    return [line for line in lines if line[bit] == most_common]


def binary_diagnostic_two(filename):
    with open(filename) as f:
        lines = []
        for line in f.readlines():
            lines.append(line.strip())

        width = len(lines[0])

        ox_lines = copy(lines)
        print(ox_lines)
        for i in range(0, width):
            ox_lines = keep_most_common(ox_lines, i)
            print(ox_lines)
            if len(ox_lines) == 1:
                break
        print(ox_lines)

        co_lines = copy(lines)
        print(co_lines)
        for i in range(0, width):
            co_lines = keep_least_common(co_lines, i)
            print(co_lines)
            if len(co_lines) == 1:
                break
        print(co_lines)
        print(int(ox_lines[0], 2) * int(co_lines[0], 2))

if __name__ == '__main__':
    binary_diagnostic_one('d3.txt')
    binary_diagnostic_two('d3.txt')
