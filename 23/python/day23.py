"""
Advent of Code 2018
Day 23: Experimental Emergency Teleportation
"""
from collections import namedtuple
from operator import attrgetter
from tqdm import tqdm

Posn = namedtuple('Posn', ['x', 'y', 'z'])
Nanobot = namedtuple('Nanobot', ['posn', 'radius'])


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


def solve_b(nanobots):
    events_x = []
    max_z_box = 0
    max_z_boxes = set()
    for n in nanobots:
        events_x.append((1, n.posn.x - n.radius, n))
        events_x.append((-1, n.posn.x + n.radius, n))
    nanobots_by_x = sorted(events_x, key=lambda a: a[1])
    box_x = set()
    for t, x, n in nanobots_by_x:
        if t == -1:
            box_x.discard(n)
        elif t == 1:
            box_x.add(n)
        events_y = []
        for n in box_x:
            events_y.append((1, n.posn.y - n.radius, n))
            events_y.append((-1, n.posn.y + n.radius, n))
        nanobots_by_y = sorted(events_y, key=lambda a: a[1])
        box_y = set()
        for t, y, n in nanobots_by_y:
            if t == -1:
                box_y.discard(n)
            elif t == 1:
                box_y.add(n)

            events_z = []
            for n in box_y:
                events_z.append((1, n.posn.z - n.radius, n))
                events_z.append((-1, n.posn.z + n.radius, n))
            nanobots_by_z = sorted(events_z, key=lambda a: a[1])
            box_z = set()
            for t, z, n in nanobots_by_z:
                if t == -1:
                    box_z.discard(n)
                    continue
                elif t == 1:
                    box_z.add(n)

                if len(box_z) > max_z_box:
                    max_z_box = len(box_z)
                    max_z_boxes = set([frozenset(box_z)])
                    # print('new', box_z, len(box_z), max_z_boxes)
                elif max_z_box and len(box_z) == max_z_box:
                    max_z_boxes.add(frozenset(box_z))
                    # print('appending', box_z, len(box_z), max_z_boxes)

    print('***')
    # for b in max_z_boxes:
        # print(b)
    print(max_z_box)


def main():
    "Main program."
    import sys
    nanobots = [parse_nanobot(ln) for ln in sys.stdin]
    # print(solve_a(nanobots))
    print(solve_b(nanobots))


if __name__ == '__main__':
    main()
