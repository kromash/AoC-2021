from copy import deepcopy


def read_scanner_reading(filename):
    scanners = []
    with open(filename) as f:
        scanner_readings = []
        for line in f.readlines():
            if line.startswith('---') or line == '\n':
                if scanner_readings:
                    scanners.append(scanner_readings)
                    scanner_readings = []
                continue
            scanner_readings.append(eval(line.strip()))
        if scanner_readings:
            scanners.append(scanner_readings)
    return scanners


def get_cord_diff(cord1, cord2):
    return tuple(cord2[i] - cord1[i] for i in range(0, 3))


def add_cords(cord1, cord2):
    return tuple(cord1[i] + cord2[i] for i in range(0, 3))


def get_diff_length(diff):
    return sum(tuple(abs(i) for i in diff))


def get_scanner_diffs(scanner):
    diff_matrix = []

    for i in range(0, len(scanner)):
        diff_matrix.append([0] * len(scanner))
        for j in range(0, len(scanner)):
            diff_matrix[i][j] = get_cord_diff(scanner[i], scanner[j])

    return diff_matrix


SIGNS_POS = [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1), (-1, -1, -1), (-1, -1, 1), (-1, 1, -1), (1, -1, -1)]


def change_orientation(cord, ord):
    return tuple(cord[i] * SIGNS_POS[ord][i] for i in range(0, 3))


def rotate(cord, rotation):
    if rotation < 3:
        return tuple(cord[rotation:]) + tuple(cord[0:rotation])
    if rotation == 3:
        return tuple([cord[0], cord[2], cord[1]])
    if rotation == 4:
        return tuple([cord[1], cord[0], cord[2]])
    if rotation == 5:
        return tuple([cord[2], cord[1], cord[0]])


def faster_is_similar(d1, d2):
    rotations = []
    for j in range(0, 6):
        d = rotate(d2, j)
        if tuple(abs(i) for i in d1) == tuple(abs(i) for i in d):
            rotations.append(j)

    return rotations


def find_similarities(m1, m2):
    l1 = len(m1)
    l2 = len(m2)
    m = []
    for i in range(l1):
        m.append([0] * l2)

    common_rotations = [0, 0, 0, 0, 0, 0]
    for i in range(l1):
        for j in range(i + 1, l1):
            for r in range(l2):
                for s in range(r + 1, l2):
                    rotations = faster_is_similar(m1[i][j], m2[r][s])
                    if rotations:
                        for rotation in rotations:
                            common_rotations[rotation] += 1
                        m[i][r] += 1
                        m[i][s] += 1
                        m[j][r] += 1
                        m[j][s] += 1

    common_beacons = {}
    for i in range(len(m)):
        line_max = max(m[i])
        if line_max:
            common_beacons[i] = m[i].index(line_max)
            print(f'{i}: {common_beacons[i]}, {line_max}')
    rotation = common_rotations.index(max(common_rotations))
    return common_beacons, rotation


def scanners_one(scanners):
    for i in range(0, len(scanners)):
        for j in range(i + 1, len(scanners)):
            diff_matrix_0 = get_scanner_diffs(scanners[i])
            diff_matrix_1 = get_scanner_diffs(scanners[j])
            print(f"find similar {i}, {j}")
            find_similarities(diff_matrix_0, diff_matrix_1)


def find_second_scanner_position(s_1, s_2, common_beacons, relative_rotation):
    for k, signs in enumerate(SIGNS_POS):
        prev = None
        aligned = 1
        for i, j in common_beacons.items():
            c_1 = s_1[i]
            c_2 = tuple(s_2[j][l] * signs[l] for l in range(0, 3))
            rotated_c_2 = rotate(c_2, relative_rotation)
            diff = get_cord_diff(rotated_c_2, c_1)
            if prev is not None:
                if diff == prev:
                    aligned += 1
                    if aligned == 12:
                        return diff, k
                else:
                    break
            else:
                prev = diff
    return [], None


def get_beacon_relative(scanner_2_r_cord, beacon_cord, orientation, rotation):
    """

    :param scanner_2_r_cord: second scanner relative cord to anchor scanner
    :param beacon_cord: beacon cord relative to scanner 2
    :param orientation: scanner 2 orientation
    :param rotation: scanner 2 rotation
    :return:
    """
    return add_cords(scanner_2_r_cord, rotate(change_orientation(beacon_cord, orientation), rotation))


checked = {0}


def recursive_compare(scanners, diff_matrix, i=0):
    global checked
    relatives = [None] * len(scanners)
    relatives[i] = (0, 0, 0)

    beacons = set(scanners[i])
    for j in range(1, len(scanners)):
        if j in checked:
            continue
        common_beacons, rotation = find_similarities(diff_matrix[i], diff_matrix[j])
        if len(common_beacons) >= 12 and rotation is not None:
            print(i, j, len(checked))
            checked.add(j)
            anchor_relatives, anchor_beacons = recursive_compare(scanners, diff_matrix, j)
            relative_coord, orientation = find_second_scanner_position(scanners[i], scanners[j], common_beacons,
                                                                       rotation)

            for beacon in anchor_beacons:
                beacons.add(get_beacon_relative(relative_coord, beacon, orientation, rotation))

            for k, relative in enumerate(anchor_relatives):
                if relative is not None:
                    print(f'calc relatives {orientation}, {rotation}')
                    relatives[k] = get_beacon_relative(relative_coord, relative, orientation, rotation)

            print(f'relative {i},{j}: {relative_coord}, {orientation}, {rotation}')
    print(f'relatives[{i}]: {relatives}')
    return relatives, beacons


if __name__ == '__main__':
    scanners = read_scanner_reading('d19.txt')
    scanners_number = len(scanners)

    scanners_relative = []
    for scanner in scanners:
        scanners_relative.append([(None, None, None)] * scanners_number)
    diff_matrix = []
    for i in range(0, len(scanners)):
        diff_matrix.append(get_scanner_diffs(scanners[i]))
    relatives, beacons = recursive_compare(scanners, diff_matrix)
    print(relatives)
    print(len(beacons))
