from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Node:
    name: str
    is_small: bool
    edges: list[str]


def read_input(filename):
    graph = {}
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            n1, n2 = line.split('-')
            for n in [n1, n2]:
                if n not in graph:
                    graph[n] = Node(n, n.islower(), [])
            graph[n1].edges.append(n2)
            graph[n2].edges.append(n1)
            print(n1, n2, n1.isupper())

    return graph


def traverse_one(graph, current, visited):
    visited[current] += 1
    if current == 'end':
        return

    for node in graph[current].edges:
        if node == 'end' or visited[node] == 0 or not graph[node].is_small:
            traverse_one(graph, node, visited)
    visited[current] -= 1


def traverse_two(graph, current, visited, v_list, visited_small_twice):
    visited[current] += 1
    v_list.append(current)
    if graph[current].is_small and visited[current] >= 2:
        visited_small_twice = True
    if current == 'end':
        print(v_list)
        v_list.pop()

        return

    for node in graph[current].edges:
        if node == 'start':
            continue
        elif node == 'end' or not graph[node].is_small:
            traverse_two(graph, node, visited, v_list, visited_small_twice)
        elif not visited_small_twice or visited[node] == 0:
            traverse_two(graph, node, visited, v_list, visited_small_twice)

    visited[current] -= 1
    v_list.pop()


def part_one(graph):
    visited = defaultdict(int)
    traverse_one(graph, 'start', visited)
    result = visited['end']
    print(f'part one answer: {result}')


def part_two(graph):
    visited = defaultdict(int)
    traverse_two(graph, 'start', visited, [], False)
    result = visited['end']
    print(f'part two answer: {result}')


if __name__ == '__main__':
    graph = read_input('d12.txt')
    # part_one(graph)
    part_two(graph)
