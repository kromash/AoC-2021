from heapq import heappush, heappop


def read_map(filename):
    with open(filename) as f:
        return [[int(num) for num in line.strip()] for line in f.readlines()]


def print_map(map):
    for row in map:
        print(''.join([str(l) for l in row]))


MOVES = [(0, 1), (1, 0), (-1, 0), (0, -1)]


def dijsktra(map):
    width = len(map[0])
    height = len(map)

    risk_map = []
    prev = []
    for i in range(0, height):
        risk_map.append([-1] * width)
        prev.append([None] * width)
    risk_map[0][0] = map[0][0]
    prev[0][0] = (0, 0)

    h = []
    heappush(h, (0, (0, 0)))
    while h:
        heap_element = heappop(h)
        curr_pos = tuple(heap_element[1])
        for move in MOVES:
            new_pos = tuple(sum(x) for x in zip(curr_pos, tuple(move)))
            if 0 <= new_pos[0] < width and 0 <= new_pos[1] < height:
                new_risk = risk_map[new_pos[0]][new_pos[1]]
                step_risk = map[new_pos[0]][new_pos[1]]
                alt_risk = risk_map[curr_pos[0]][curr_pos[1]] + step_risk
                if new_risk == -1 or alt_risk < new_risk:
                    risk_map[new_pos[0]][new_pos[1]] = alt_risk
                    prev[new_pos[0]][new_pos[1]] = curr_pos

                    heappush(h, (alt_risk, new_pos))


    print(risk_map[width - 1][height - 1] - risk_map[0][0])


def chiton_one(filename):
    map = read_map(filename)
    dijsktra(map)


def make_bigger_map(map):
    width = len(map[0])
    height = len(map)
    big_width = width * 5
    big_height = height * 5
    bigger_map = []
    for i in range(0, big_height):
        bigger_map.append([0] * big_width)
    for i in range(0, 5):
        for j in range(0, 5):
            for k in range(width):
                for l in range(height):
                    new = map[k][l] + i + j
                    if new > 9:
                        new -= 9
                    bigger_map[k + (i * width)][l + (j * height)] = new
    return bigger_map


def chiton_two(filename):
    map = read_map(filename)
    bigger_map = make_bigger_map(map)
    dijsktra(bigger_map)


if __name__ == '__main__':
    chiton_one('d15.txt')
    chiton_two('d15.txt')
