"""
Advent of Code 2018
Day 8: Memory Maneuver
"""
from collections import deque, namedtuple

Node = namedtuple('Node', ['n_children', 'children', 'n_metadata', 'metadata'])

def build_tree(data):
    "Build the tree"
    # print(data)
    n_children = data.popleft()
    n_metadata = data.popleft()
    # print(n_children, n_metadata)
    metadata = []
    if n_children:
        for _ in range(n_metadata):
            metadata.append(data.pop())
    else:
        for _ in range(n_metadata):
            metadata.append(data.popleft())
    children = []
    for _ in range(n_children):
        children.append(build_tree(data))
    return Node(n_children, children, n_metadata, metadata)


def solveA(tree):
    "Solve first part of puzzle."
    return sum(tree.metadata) + sum(solveA(c) for c in tree.children)


def main():
    "Main program."
    import sys
    sys.setrecursionlimit(30000)
    data = deque([int(i) for i in sys.stdin.read().split()])
    print(len(data))
    tree = build_tree(data)
    print(solveA(tree))


if __name__ == '__main__':
    main()

