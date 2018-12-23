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
    max_coords = None
    for n in nanobots:
        events_x.append((1, n.posn.x - n.radius, n))
        events_x.append((-1, n.posn.x + n.radius, n))
    nanobots_by_x = sorted(events_x, key=lambda a: a[1])
    box_x = set()
    for (tx, x, nx), (tx0, x0, nx0) in tqdm(list(zip(nanobots_by_x[:-1],nanobots_by_x[1:]))):
        if tx == -1:
            box_x.discard(nx)
        elif tx == 1:
            box_x.add(nx)
        if len(box_x) < max_z_box:
            continue
        events_y = []
        for n in box_x:
            events_y.append((1, n.posn.y - n.radius, n))
            events_y.append((-1, n.posn.y + n.radius, n))
        nanobots_by_y = sorted(events_y, key=lambda a: a[1])
        box_y = set()
        for (ty, y, ny), (ty0, y0, ny0) in zip(nanobots_by_y[:-1], nanobots_by_y[1:]):
            if ty == -1:
                box_y.discard(ny)
            elif ty == 1:
                box_y.add(ny)

            if len(box_y) < max_z_box:
                continue

            events_z = []
            for n in box_y:
                events_z.append((1, n.posn.z - n.radius, n))
                events_z.append((-1, n.posn.z + n.radius, n))
            nanobots_by_z = sorted(events_z, key=lambda a: a[1])
            box_z = set()
            for (tz, z, nz), (tz0, z0, nz0) in zip(nanobots_by_z[:-1], nanobots_by_z[1:]):
                if tz == -1:
                    box_z.discard(nz)
                    continue
                elif tz == 1:
                    box_z.add(nz)

                if len(box_z) > max_z_box:
                    max_z_box = len(box_z)
                    max_coords = ((x, x0), (y, y0), (z, z0))
                    if max_z_box == 971 or max_z_box == 5:
                        print('max_z_box', max_z_box, 'x', x, 'x0', x0, 'y', y, 'y0', y0, 'z', z, 'z0', z0)
                        print('x', nx0, nx0.posn.x + nx0.radius, nx0.posn.y + nx0.radius, nx0.posn.z + nx0.radius)
                        print('y', ny0, ny0.posn.x + ny0.radius, ny0.posn.y + ny0.radius, ny0.posn.z + ny0.radius)
                        print('z', nz0, nz0.posn.x + nz0.radius, nz0.posn.y + nz0.radius, nz0.posn.z + nz0.radius)
                        print(box_z)


    print('***')
    print(max_z_box)
    (x0, x1), (y0, y1), (z0, z1) = max_coords


def main():
    "Main program."
    import sys
    nanobots = [parse_nanobot(ln) for ln in sys.stdin]
    print(len(nanobots), 'nanobots')
    # print(solve_a(nanobots))
    print(solve_b(nanobots))


if __name__ == '__main__':
    main()
