"""
Advent of Code 2018
Day 17: Reservoir Research
"""
from collections import namedtuple
from math import inf

Vein = namedtuple('Vein', ['minx', 'maxx', 'miny', 'maxy'])
Posn = namedtuple('Posn', ['x', 'y'])

EMPTY_SPACE = ' '

def print_grid(grid):
    print("\n".join("".join(r) for r in grid))

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
    return grid, Posn(spring_x, spring_y)


def fill_down(grid, posn):
    "Find what is down."
    # print('fill_down', posn)
    while posn.y + 1 < len(grid) and grid[posn.y + 1][posn.x] == EMPTY_SPACE:
        grid[posn.y + 1][posn.x] = '~'
        posn = Posn(posn.x, posn.y + 1)
    if posn.y + 1 < len(grid):
        return grid[posn.y + 1][posn.x], posn
    else:
        return '!', posn


def fill_left(grid, posn):
    "Find what is left."
    print('fill_left', posn)
    while grid[posn.y][posn.x - 1] == EMPTY_SPACE and grid[posn.y + 1][posn.x - 1] in ['#', '~']:
        grid[posn.y][posn.x - 1] = '~'
        posn = Posn(posn.x - 1, posn.y)
    if grid[posn.y][posn.x - 1] == EMPTY_SPACE:
        grid[posn.y][posn.x - 1] = '~'
        return EMPTY_SPACE, Posn(posn.x - 1, posn.y)
    return grid[posn.y][posn.x - 1], posn


def fill_right(grid, posn):
    "Find what is right."
    print('fill_right', posn)
    while grid[posn.y][posn.x + 1] == EMPTY_SPACE and grid[posn.y + 1][posn.x + 1] in ['#', '~']:
        grid[posn.y][posn.x + 1] = '~'
        posn = Posn(posn.x + 1, posn.y)
    if grid[posn.y][posn.x + 1] == EMPTY_SPACE:
        grid[posn.y][posn.x + 1] = '~'
        return EMPTY_SPACE, Posn(posn.x + 1, posn.y)
    return grid[posn.y][posn.x + 1], posn

def fill(grid, posn):
    queue = [posn]
    while queue:
        new_queue = []
        for posn in queue:
            print("P", posn)
            marker0, posn0 = fill_down(grid, posn)
            if marker0 == '!':
                continue
            marker1, posn1 = fill_left(grid, posn0)
            print(posn1, 'left marker', marker1)
            if marker1 == EMPTY_SPACE:
                new_queue.append(posn1)
            marker2, posn2 = fill_right(grid, posn0)
            print(posn2, 'right marker', marker2)
            if marker2 == EMPTY_SPACE:
                new_queue.append(posn2)
            if marker1 != EMPTY_SPACE and marker2 != EMPTY_SPACE:
                new_queue.append(Posn(posn0.x, posn0.y - 1))
        queue = new_queue
        print_grid(grid)


def fill0(grid, posn):
    path = [posn]
    for _ in range(5):
        print_grid(grid)
        print(path)
        # Down?
        posn = path[-1]
        print(posn, len(grid), len(grid[0]))
        while posn.y + 1 < len(grid) and grid[posn.y + 1][posn.x] == EMPTY_SPACE:
            print('dn', posn)
            grid[posn.y + 1][posn.x] = '~'
            posn = Posn(posn.x, posn.y)
        if posn.y >= len(grid):
            path.pop()
            continue

        if posn != path[-1]:
            path.append(Posn(posn.x, posn.y + 1))
            continue

        # Left?
        posn = path[-1]
        while grid[posn.y][posn.x - 1] == EMPTY_SPACE:
            grid[posn.y][posn.x - 1] = '~'
            if grid[posn.y + 1][posn.x - 1] == EMPTY_SPACE:
                break
            posn = Posn(posn.x + 1, posn.y)
        if grid[posn.y + 1][posn.x - 1] == EMPTY_SPACE:
            path.append(Posn(posn.x + 1, posn.y))
            continue

        # Right?
        posn = path[-1]
        while grid[posn.y][posn.x + 1] == EMPTY_SPACE:
            grid[posn.y][posn.x + 1] = '~'
            if grid[posn.y + 1][posn.x + 1] == EMPTY_SPACE:
                break
            posn = Posn(posn.x + 1, posn.y)
        if grid[posn.y + 1][posn.x + 1] == EMPTY_SPACE:
            path.append(Posn(posn.x + 1, posn.y))
            continue

        path.pop()





def solve_a(veins):
    "Solve first part of puzzle."
    grid, spring = new_map(veins)
    fill0(grid, spring)
    soln = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] in ['~', '|', '-']:
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
