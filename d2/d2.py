def dive_one(filename):
    horizontal = 0
    depth = 0
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            print(line)
            if line.startswith('up'):
                print(f'up: {line[2:]}')
                depth -= int(line[2:].strip())
            if line.startswith('down'):
                print(f'up: {line[4:]}')
                depth += int(line[4:].strip())
            if line.startswith('forward'):
                print(f'forward: {line[7:]}')
                horizontal += int(line[7:].strip())
    print(depth, horizontal, depth * horizontal)


def dive_two(filename):
    horizontal = 0
    aim = 0
    depth = 0
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            print(line)
            if line.startswith('up'):
                print(f'up: {line[2:]}')
                aim -= int(line[2:].strip())
            if line.startswith('down'):
                print(f'up: {line[4:]}')
                aim += int(line[4:].strip())
            if line.startswith('forward'):
                print(f'forward: {line[7:]}')
                value = int(line[7:].strip())
                horizontal += value
                depth += aim * value
    print(depth, horizontal, depth * horizontal)


if __name__ == '__main__':
    dive_one('d2.txt')
    dive_two('d2.txt')
