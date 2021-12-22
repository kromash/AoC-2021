from collections import defaultdict
from copy import deepcopy


def read_input(filename):
    with open(filename) as f:
        lines = f.readlines()

    pattern = lines[0].strip()
    rules = {}
    for line in lines[1:]:
        if len(line) > 3:
            rules[line[0:2]] = line[6]

    return pattern, rules


def add_dicts(d1, d2):
    result = deepcopy(d1)
    for key, value in d2.items():
        result[key] = result.get(key, 0) + value

    return result


def recreate_steps(start, steps, dynamic_patterns):
    global max_steps
    counts = defaultdict(int)
    if steps == 0:
        for letter in start:
            counts[letter] += 1
        return counts

    if len(start) == 2 and dynamic_patterns[start][steps]:
        return dynamic_patterns[start][steps]
    result = {}
    for i in range(0, len(start) - 1):
        pair = start[i] + start[i + 1]
        # print(pair)
        pair_insertion = pair[0] + rules[pair] + pair[1]

        left_key = pair_insertion[0:2]
        right_key = pair_insertion[1:3]

        left = recreate_steps(left_key, steps - 1, dynamic_patterns)
        right = recreate_steps(right_key, steps - 1, dynamic_patterns)
        dynamic_patterns[left_key][steps - 1] = left
        dynamic_patterns[right_key][steps - 1] = right

        # print(left + right[1:-1])
        dicts_sum = add_dicts(left, right)
        dicts_sum[rules[pair]] -= 1
        result = add_dicts(result, dicts_sum)
        result[pair[1]] -= 1

    if steps > max_steps:
        max_steps = steps
    result[start[-1]] += 1
    return result


def polymerization(pattern, rules, steps):
    dynamic_patterns = {}

    for fr, to in rules.items():
        dynamic_patterns[fr] = [None] * steps
        dynamic_patterns[fr][0] = fr

    result = recreate_steps(pattern, steps, dynamic_patterns)
    print(max(result.values()) - min(result.values()))


def polymerization_one(pattern, rules):
    polymerization(pattern, rules, 10)


def polymerization_two(pattern, rules):
    polymerization(pattern, rules, 40)


if __name__ == '__main__':
    pattern, rules = read_input('d14.txt')
    max_steps = 0
    polymerization_one(pattern, rules)
    polymerization_two(pattern, rules)
