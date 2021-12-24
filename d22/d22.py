import re
from itertools import product

import numpy as np
import portion as P
from intervaltree import IntervalTree
from portion import Interval as PortionInterval


def parse_line(line):
    # on x=-20..26,y=-36..17,z=-47..7
    m = re.match(r'(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)', line.strip()).groups()
    return [1 if m[0] == 'on' else 0, (int(m[1]), int(m[2])), (int(m[3]), int(m[4])), (int(m[5]), int(m[6]))]


def read_input(filename):
    input = []
    with open(filename) as f:
        for line in f.readlines():
            input.append(parse_line(line))

    print(input)
    return input


def part_one(input):
    grid = np.zeros([101, 101, 101])
    # grid[(1:5), 2:6, 2:8] = 1

    print(np.sum(grid))

    for area in input:
        coords = []
        for coord in area[1:4]:
            coords.extend([abs(coord[0]), abs(coord[1])])

        if max(coords) > 50:
            continue
        moved_coords = []
        for coord in area[1:4]:
            moved_coords.extend([coord[0] + 50, coord[1] + 51])
        print(moved_coords)
        grid[moved_coords[0]:moved_coords[1], moved_coords[2]:moved_coords[3], moved_coords[4]:moved_coords[5]] = area[
            0]

    result = np.sum(grid)
    print(f'part one answer: {int(result)}')


class Cuboid:
    def __init__(self, x, y, z):
        if isinstance(x, PortionInterval):
            x = [x.lower, x.upper]
        if isinstance(y, PortionInterval):
            y = [y.lower, y.upper]
        if isinstance(z, PortionInterval):
            z = [z.lower, z.upper]
        self.x = P.closed(*x)
        self.y = P.closed(*y)
        self.z = P.closed(*z)

    def as_list(self):
        return [self.x, self.y, self.z]

    def __str__(self):
        return f'c: {self.x}, {self.y}, {self.z}'

    def inside(self, other):
        return other.x in self.x and other.y in self.y and other.z in self.z

    @staticmethod
    def _sub(a: PortionInterval, b: PortionInterval):
        s = a - b
        if s.empty:
            return s
        return [r.replace(left=P.CLOSED, right=P.CLOSED,
                          lower=r.lower + 1 * (r.left == P.OPEN), upper=r.upper - 1 * (r.right == P.OPEN)) for r in s]

    def __add__(self, other):
        in_x = self.x & other.x
        in_y = self.y & other.y
        in_z = self.z & other.z

        if other.inside(self):
            return [other]
        if self.inside(other):
            return [self]

        if other.x in self.x and other.y in self.y and other.z in self.z:
            return [self]
        if not in_x.empty and not in_y.empty and not in_z.empty:
            results = []  # Cuboid(in_x, in_y, in_z)]
        else:
            return [self, other]
        inter = []
        so = []
        os = []
        for s, o in zip(self.as_list(), other.as_list()):
            # if not(s - o).empty:
            so.append(self._sub(s, o))
            # if not (o - s).empty:
            os.append(self._sub(o, s))
            inter.append(o & s)

        parts_s = [[], [], []]
        parts_o = [[], [], []]
        for i in range(0, 3):
            parts_s[i].append(inter[i])
            parts_o[i].append(inter[i])
            for k in list(so[i]):
                if not k.empty:
                    parts_s[i].append(k)
            for k in list(os[i]):
                if not k.empty:
                    parts_o[i].append(k)
        p_s = list(product(*parts_s))
        p_o = list(product(*parts_o))

        if p_s[0] == p_o[0]:
            results.append(Cuboid(*p_s[0]))
        else:
            print("ERRRORRORORO")
        for s in p_s[1:]:
            results.append(Cuboid(*s))
        for o in p_o[1:]:
            results.append(Cuboid(*o))

        return results

    def __sub__(self, other):
        inter = []
        so = []
        for s, o in zip(self.as_list(), other.as_list()):
            inter.append(o & s)

        if any([i.empty for i in inter]):
            return [self]

        for s, o in zip(self.as_list(), other.as_list()):
            so.append(self._sub(s, o))

        results = []
        parts_s = [[], [], []]
        for i in range(0, 3):
            parts_s[i].append(inter[i])
            for k in list(so[i]):
                if not k.empty:
                    parts_s[i].append(k)

        p_s = list(product(*parts_s))

        for s in p_s[1:]:
            results.append(Cuboid(*s))
        return results

    def area(self):
        return self._len(self.x) * self._len(self.y) * self._len(self.z)

    @staticmethod
    def _len(interval: P):
        return interval.upper - interval.lower + 1


def part_two(input):
    tree = IntervalTree()
    for input_cube in input:
        print(f'input cube: {input_cube}, {len(tree)}')
        input_cuboid = Cuboid(input_cube[1], input_cube[2], input_cube[3])
        in_range = tree.overlap(input_cube[1][0], input_cube[1][1] + 1)

        tree.remove_overlap(input_cube[1][0], input_cube[1][1] + 1)
        new_cubes = IntervalTree()
        for cube in in_range:
            for new_cube in cube.data - input_cuboid:
                new_cubes[new_cube.x.lower:new_cube.x.upper + 1] = new_cube
        if input_cube[0] == 1:
            new_cubes[input_cuboid.x.lower:input_cuboid.x.upper + 1] = input_cuboid

        if new_cubes:
            tree |= new_cubes

    area_sum = 0
    for e in tree:
        area_sum += e.data.area()

    print(f'part two answer: {area_sum}')


if __name__ == '__main__':
    input = read_input('d22.txt')

    part_two(input)
