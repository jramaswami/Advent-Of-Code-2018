"""
Advent of Code 2018
Day 23: Experimental Emergency Teleportation
"""
from collections import namedtuple, defaultdict
from operator import attrgetter


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


def get_maximal_clique(overlapping_spheres, nanobots):
    "Return the maximal clique."
    clique = set([nanobots[0]])
    for nanobot in overlapping_spheres:
        if nanobot in clique:
            continue
        elif all(n in overlapping_spheres[nanobot] for n in clique):
            clique.add(nanobot)
    return clique


def solve_b(nanobots):
    "Solve second part of puzzle."
    # Look for overlapping spheres
    overlapping_spheres = defaultdict(set)
    for n0 in nanobots:
        for n1 in nanobots:
            if n1 == n0:
                continue
            if manhattan_distance(n0, n1) <= n0.radius + n1.radius:
                overlapping_spheres[n0].add(n1)

    farthest_distance = 0
    #  Look for maximal clique
    maximal_clique = get_maximal_clique(overlapping_spheres, nanobots)
    # Compute max distance in clique
    for nanobot in maximal_clique:
        # d = manhattan_distance_pt(Posn(0, 0, 0), n) - n.radius
        distance = sum(abs(p) for p in nanobot.posn) - nanobot.radius
        if distance > farthest_distance:
            farthest_distance = distance
    return farthest_distance


def main():
    "Main program."
    import sys
    nanobots = [parse_nanobot(ln) for ln in sys.stdin]
    print(solve_a(nanobots))
    print(solve_b(nanobots))


if __name__ == '__main__':
    main()
