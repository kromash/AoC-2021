def read_input(filename):
    with open(filename) as f:
        lines = f.readlines()

    return [int(line.strip()) for line in lines]


def sonar_one(sonar):
    incr = 0
    prev = sonar[0]
    for v in sonar[1:]:
        if v > prev:
            incr += 1
        prev = v

    print(incr)


def part_two(sonar):
    incr = 0
    prev_window_sum = sum(sonar[0:3])
    for i, v in enumerate(sonar[3:]):
        window_sum = prev_window_sum + v - sonar[i]
        if window_sum > prev_window_sum:
            incr += 1

    print(incr)


if __name__ == '__main__':
    sonar = read_input('d1.txt')
    part_two(sonar)
