"""
Advent of Code 2018
Day 17: Reservoir Research
"""
from collections import namedtuple
from math import inf

Vein = namedtuple('Vein', ['minx', 'maxx', 'miny', 'maxy'])
Map = namedtuple('Map', ['grid', 'xoff', 'spring_x'])
Posn = namedtuple('Posn', ['x', 'y'])

EMPTY_SPACE = ' '
def parse_scan(input_line):
    "Parse a scan from input line."
    tokens = input_line.strip().split(', ')
    for t in tokens:
        label = t[0]
        coords = t[2:].split('..')
        if len(coords) == 1:
            coords.append(coords[0])
        if label == 'x':
            minx = int(coords[0])
            maxx = int(coords[1])
        elif label == 'y':
            miny = int(coords[0])
            maxy = int(coords[1])
    return Vein(minx, maxx, miny, maxy)


def new_map(veins):
    "Make a map."
    minx = inf
    maxx = -inf
    maxy = -inf
    for vn in veins:
        minx = min(vn.minx, minx)
        maxx = max(vn.maxx, maxx)
        maxy = max(vn.maxy, maxy)
    wd = maxx - minx + 3
    xoff = minx - 1
    ht = maxy + 1
    grid = [[EMPTY_SPACE for _ in range(wd)] for _ in range(ht)]
    for vn in veins:
        for y in range(vn.miny, vn.maxy + 1):
            for x in range(vn.minx, vn.maxx + 1):
                grid[y][x - xoff] = '#'

    spring_x, spring_y = 500 - xoff, 0
    grid[spring_y][spring_x] = '+'
    return Map(grid, xoff, spring_x)

def neighborhood(grid, posn):
    "Return neighbors."
    offsets = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    neighbors = []
    for dy, dx in offsets:
        x = posn.x + dx
        y = posn.y + dy
        if x >= 0 and x < len(grid[0]) \
        and y >= 0 and y <= len(grid) \
        and grid[y][x] != '#':
            neighbors.append(Posn(x, y))
    return neighbors


# TODO: Fill strategy does needs to change.
def fill(mp):
    queue = [Posn(mp.spring_x, 0)]
    while queue:
        new_queue = []
        for posn in queue:
            me = mp.grid[posn.y][posn.x]
            if me == '+' or me == '|':
                # down
                while posn.y + 1 < len(mp.grid) and mp.grid[posn.y + 1][posn.x] == EMPTY_SPACE:
                    mp.grid[posn.y + 1][posn.x] = '|'
                    posn = Posn(posn.x, posn.y + 1)
                if posn.y < len(mp.grid) - 1:
                    mp.grid[posn.y][posn.x] = '-'
                    new_queue.append(Posn(posn.x, posn.y))
            elif me == '-':
                posnr = Posn(posn.x, posn.y)
                while mp.grid[posnr.y + 1][posnr.x] != EMPTY_SPACE and mp.grid[posnr.y][posnr.x + 1] == EMPTY_SPACE:
                    mp.grid[posnr.y][posnr.x + 1] = '-'
                    posnr = Posn(posnr.x + 1, posnr.y)

                posnl = Posn(posn.x, posn.y)
                while mp.grid[posnl.y + 1][posnl.x] != EMPTY_SPACE and mp.grid[posnl.y][posnl.x - 1] == EMPTY_SPACE:
                    mp.grid[posnl.y][posnl.x - 1] = '-'
                    posnl = Posn(posnl.x - 1, posnl.y)

                # TODO: change this to go left/right as far as possible instead of between them
                #       may have to add something to skip queued water.
                if mp.grid[posnr.y + 1][posnr.x] != EMPTY_SPACE and mp.grid[posnl.y + 1][posnl.x] != EMPTY_SPACE:
                    x = posnl.x
                    while mp.grid[posnl.y][x] == '-':
                        mp.grid[posnl.y][x] = '~'
                        if mp.grid[posnl.y - 1][x] == '|':
                            new_queue.append(Posn(x, posnl.y - 1))
                            mp.grid[posnl.y - 1][x] = '-'
                        x += 1

                    x = posnl.x
                    while mp.grid[posnr.y][x] == '-':
                        mp.grid[posnr.y][x] = '~'
                        if mp.grid[posnr.y - 1][x] == '|':
                            new_queue.append(Posn(x, posnr.y - 1))
                            mp.grid[posnr.y - 1][x] = '-'
                        x -= 1

#                     for x in range(posnl.x, posnr.x + 1):
                        # mp.grid[posnl.y][x] = '~'
                        # if mp.grid[posnl.y - 1][x] == '|':
                            # mp.grid[posnl.y - 1][x] = '-'
                            # new_queue.append(Posn(x, posnl.y - 1))

                if mp.grid[posnr.y + 1][posnr.x] == EMPTY_SPACE:
                    mp.grid[posnr.y][posnr.x] = '|'
                    new_queue.append(posnr)

                if mp.grid[posnl.y + 1][posnl.x] == EMPTY_SPACE:
                    mp.grid[posnl.y][posnl.x] = '|'
                    new_queue.append(posnl)
        queue = new_queue
    print("\n".join("".join(r) for r in mp.grid))
    print('END')


def fill0(grid, spring):
    posn = Posn(spring.x, spring.y + 1)
    grid[posn.y][posn.x] = '~'
    path = [spring]
    visited = set([spring])
    # for _ in range(50):
    while path:
        print(posn, grid[posn.y][posn.x])
        print("L|{}|".format(grid[posn.y][posn.x - 1]), "R|{}|".format(grid[posn.y][posn.x + 1]))
        print("\n".join("".join(r) for r in grid))
        print()

        if posn.y + 1 >= len(grid):
            grid[posn.y][posn.x] = '|'
            while grid[posn.y][posn.x] == '|':
                print('backtracking', posn)
                posn = path.pop()
            print('arrived', posn)
        elif grid[posn.y + 1][posn.x] == EMPTY_SPACE:
            # down
            path.append(posn)
            grid[posn.y][posn.x] = '|'
            posn = Posn(posn.x, posn.y + 1)
        elif grid[posn.y][posn.x + 1] == EMPTY_SPACE:
            # right
            path.append(posn)
            grid[posn.y][posn.x] = '-'
            posn = Posn(posn.x + 1, posn.y)
        elif grid[posn.y][posn.x - 1] == EMPTY_SPACE:
            path.append(posn)
            grid[posn.y][posn.x] = '-'
            posn = Posn(posn.x - 1, posn.y)
        else:
            while grid[posn.y][posn.x + 1] != EMPTY_SPACE and grid[posn.y][posn.x - 1] != EMPTY_SPACE:
                print('backtracking', posn)
                grid[posn.y][posn.x] = '~'
                posn = path.pop()
            print('arrived', posn)
        visited.add(posn)

    print("\n".join("".join(r) for r in grid))
    print()



def solve_a(veins):
    "Solve first part of puzzle."
    mp = new_map(veins)
    fill0(mp.grid, Posn(mp.spring_x, 0))
    soln = 0
    for y in range(len(mp.grid)):
        for x in range(len(mp.grid[0])):
            if mp.grid[y][x] in ['~', '|', '-']:
                soln += 1
    return soln



def solve_b():
    "Solve second part of puzzle."
    pass


def main():
    "Main program."
    import sys
    veins = [parse_scan(ln) for ln in sys.stdin]
    print(solve_a(veins))


if __name__ == '__main__':
    main()
