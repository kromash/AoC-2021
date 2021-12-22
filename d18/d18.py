from math import floor, ceil
from typing import Optional

from binarytree import Node, NodeValue


class TNode(Node):
    def __init__(
            self,
            value: NodeValue,
            left: Optional["Node"] = None,
            right: Optional["Node"] = None,
            parent: Optional["Node"] = None
    ) -> None:
        self.parent = parent
        super().__init__(value, left, right)

    def is_leaf(self):
        return self.left is None and self.right is None


def read_numbers(filename):
    with open(filename, 'r') as f:
        for line in f.readlines():
            yield eval(line.strip())


def create_tree(s_number):
    if isinstance(s_number, list) and len(s_number) == 0:
        return TNode(0)
    if isinstance(s_number, int):
        return TNode(s_number)
    node = TNode(0)
    # print(f'c: {s_number}')
    node.left = create_tree(s_number[0])
    node.right = create_tree(s_number[1])
    node.left.parent = node
    node.right.parent = node
    return node


def add_trees(left, right):
    root = TNode(0)
    root.left = left
    root.right = right
    root.left.parent = root
    root.right.parent = root

    return reduce(root)


def search_for_explode(root, depth=0):
    res = None
    if root.left:
        res = search_for_explode(root.left, depth + 1)

    if root.right and not res:
        res = search_for_explode(root.right, depth + 1)

    if res is True:
        return root
    if res:
        return res

    if root.is_leaf():
        if depth > 4:
            return True

    return None


def find_left_neighbour(root, node):
    _prev = None
    for _node in root.postorder:
        if _node == node:
            return _prev
        if _node.is_leaf():
            _prev = _node
    return None


def find_right_neighbour(root, node):
    postoreder = root.postorder
    for i, _node in enumerate(postoreder):
        if _node == node:
            for next_node in postoreder[i + 1:]:
                if next_node.is_leaf():
                    return next_node

            return None
    return None


def explode(root, node):
    left_value = node.left.value
    right_value = node.right.value
    node.left = None
    node.right = None
    left = find_left_neighbour(root, node)
    right = find_right_neighbour(root, node)

    if left:
        left.value += left_value
    if right:
        right.value += right_value


def split(root):
    if not root.is_leaf():
        res = split(root.left)
        if res:
            return res
        res = split(root.right)
        if res:
            return res

    if root.value >= 10:
        root.left = TNode(value=floor(root.value / 2), parent=root)
        root.right = TNode(value=ceil(root.value / 2), parent=root)
        root.value = 0
        return True
    return False


def reduce(root):
    to_explode = search_for_explode(root)
    while to_explode:
        explode(root, to_explode)
        to_explode = search_for_explode(root)
    if split(root):
        return reduce(root)
    return root


def get_magnitude(root):
    value = 0
    if root.is_leaf():
        return root.value
    if root.left:
        value += 3 * get_magnitude(root.left)
    if root.right:
        value += 2 * get_magnitude(root.right)
    return value


def snailfish_one(filename):
    t = create_tree([])
    for number in read_numbers(filename):
        t = add_trees(t, create_tree(number))
    print(t)
    print(get_magnitude(t))


def snailfish_two(filename):
    numbers = list(read_numbers(filename))
    max_magnitude = 0
    for i in range(0, len(numbers)):
        for j in range(0, len(numbers)):
            if i != j:
                print(i, j)
                t1 = create_tree(numbers[i])
                t2 = create_tree(numbers[j])
                t = add_trees(t1, t2)
                magnitude = get_magnitude(t)
                if magnitude > max_magnitude:
                    max_magnitude = magnitude

    print(max_magnitude)


if __name__ == '__main__':
    snailfish_one('d18.txt')
    snailfish_two('d18.txt')
