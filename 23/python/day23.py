"""
Advent of Code 2018
Day 23: Experimental Emergency Teleportation
"""
from collections import namedtuple, defaultdict
from operator import attrgetter
from tqdm import tqdm

Posn = namedtuple('Posn', ['x', 'y', 'z'])
Nanobot = namedtuple('Nanobot', ['posn', 'radius'])


def manhattan_distance_pt(posn, nanobot):
    "Return manhattan distance between point and nanobot."
    return abs(posn.x - nanobot.posn.x) + \
           abs(posn.y - nanobot.posn.y) + \
           abs(posn.z - nanobot.posn.z)

def manhattan_distance(nanobot0, nanobot1):
    "Return manhattan distance between nanobots."
    return abs(nanobot0.posn.x - nanobot1.posn.x) + \
           abs(nanobot0.posn.y - nanobot1.posn.y) + \
           abs(nanobot0.posn.z - nanobot1.posn.z)


def in_range(nanobot0, nanobot1):
    "Return True if nanobot1 is in range of nanobot0."
    return manhattan_distance(nanobot0, nanobot1) <= nanobot0.radius


def parse_nanobot(line):
    "Parse a nanobot description."
    left_bracket = line.find('<')
    right_bracket = line.find('>')
    posn = Posn(*(int(i) for i in line[left_bracket+1:right_bracket].split(',')))
    right_equal = line.rfind('=')
    radius = int(line[right_equal+1:])
    return Nanobot(posn, radius)


def solve_a(nanobots):
    "Solve first part of puzzle."
    nanobot0 = max(nanobots, key=attrgetter('radius'))
    return sum(1 for n in nanobots if in_range(nanobot0, n))


def maximal_clique(cxs, nanobots):
    max_cq = None
    max_len = 0
    for start in nanobots:
        clique = set([start])
        for v in cxs:
            if v in clique:
                continue
            elif all(u in cxs[v] for u in clique):
                clique.add(v)

        if len(clique) > max_len:
            max_len = len(clique)
            max_cq = clique

    return max_cq


def solve_b(nanobots):
    "Solve second part of puzzle."
    cxs = defaultdict(set)
    for n0 in nanobots:
        for n1 in nanobots:
            if n1 == n0:
                continue
            if manhattan_distance(n0, n1) <= n0.radius:
                cxs[n0].add(n1)

    nn = None
    nd = 0
    mx_cq = maximal_clique(cxs, nanobots)
    print(mx_cq)
    for n in mx_cq:
        d = manhattan_distance_pt(Posn(0, 0, 0), n) - n.radius
        if d > nd:
            nn = n
            nd = d
        print(n, d)
    print('$', nn, nd)



def main():
    "Main program."
    import sys
    nanobots = [parse_nanobot(ln) for ln in sys.stdin]
    print(len(nanobots), 'nanobots')
    # print(solve_a(nanobots))
    print(solve_b(nanobots))

if __name__ == '__main__':
    main()
