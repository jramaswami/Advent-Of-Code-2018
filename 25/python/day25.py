"""
Advent of Code 2018
Day 25: Four-Dimensional Adventure
"""
from collections import namedtuple, defaultdict
from itertools import combinations

Point = namedtuple('Point', ['x', 'y', 'z', 't'])

def parse_point(line):
    "Parse a point from an input line."
    return Point(*(int(i) for i in line.strip().split(',')))

def manhattan_distance(pt0, pt1):
    "Return manhattan distance between points."
    return sum(abs(ls - rs) for ls, rs in zip(pt0, pt1))

def solve_a(points):
    "Solve first part of puzzle."
    adj = defaultdict(list)
    for p0, p1 in combinations(points, 2):
        if manhattan_distance(p0, p1) <= 3:
            adj[p0].append(p1)
            adj[p1].append(p0)

    constellations = 0
    visited = set()
    for p0 in points:
        if p0 in visited:
            continue
        constellations += 1
        queue = [p0]
        while queue:
            u = queue.pop()
            visited.add(u)
            for v in adj[u]:
                if v not in visited:
                    queue.append(v)
    return constellations


def main():
    "Main program."
    import sys
    points = [parse_point(ln) for ln in sys.stdin]
    print(solve_a(points))


if __name__ == '__main__':
    main()
