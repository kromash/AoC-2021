from math import ceil, floor


def read_input(filename):
    input = []
    with open(filename) as f:
        for line in f.readlines():
            input.append(line.strip())

    return input


def check_chunks(chunks):
    open_braces = []
    for c in chunks:
        if c in ['[', '(', '{', '<']:
            open_braces.append(c)
        else:
            last_open = open_braces.pop()
            if c == ')' and last_open != '(':
                return 3
            if c == ']' and last_open != '[':
                return 57
            if c == '}' and last_open != '{':
                return 1197
            if c == '>' and last_open != '<':
                return 25137
    return 0

def complete_chunks(chunks):
    open_braces = []
    for c in chunks:
        if c in ['[', '(', '{', '<']:
            open_braces.append(c)
        else:
            last_open = open_braces.pop()
            if c == ')' and last_open != '(':
                return 0
            if c == ']' and last_open != '[':
                return 0
            if c == '}' and last_open != '{':
                return 0
            if c == '>' and last_open != '<':
                return 0
    result = 0
    while open_braces:
        c = open_braces.pop()
        result = result * 5 + ['(', '[', '{', '<'].index(c)+1
    return result

def part_one(input):
    result = 0
    print(input)
    for chunk in input:
        result += check_chunks(chunk)
    print(f'part one answer: {result}')


def part_two(input):
    results = []
    for chunk in input:
        value = complete_chunks(chunk)
        if value:
            results.append(value)
    results.sort()
    result = results[floor(len(results)/2)]
    print(f'part two answer: {result}')


if __name__ == '__main__':
    input = read_input('d10.txt')
    #part_one(input)
    part_two(input)
