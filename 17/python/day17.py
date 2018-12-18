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
    print()

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
    miny = inf
    maxy = -inf
    for vn in veins:
        minx = min(vn.minx, minx)
        maxx = max(vn.maxx, maxx)
        miny = min(vn.miny, miny)
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
    return grid, Posn(spring_x, spring_y), miny, maxy


def move_up(grid, posn):
    if posn.y - 1 > 0:
        return Posn(posn.x, posn.y - 1)

def move_down(grid, posn):
    if posn.y + 1 < len(grid):
        return Posn(posn.x, posn.y + 1)

def move_left(grid, posn):
    if posn.x - 1 >= 0:
        return Posn(posn.x - 1, posn.y)

def move_right(grid, posn):
    if posn.x + 1 < len(grid[0]):
        return Posn(posn.x + 1, posn.y)

def grid_get(grid, posn):
    return grid[posn.y][posn.x]

def grid_set(grid, posn, cell):
    grid[posn.y][posn.x] = cell

def fill_between(grid, left, right, cell="~"):
    for x in range(left.x + 1, right.x):
        grid_set(grid, Posn(x, left.y), cell)

def find_left(grid, posn):
    under = move_down(grid, posn)
    if grid_get(grid, under) == '|' or grid_get(grid, under) == EMPTY_SPACE:
        return posn
    posn = move_left(grid, posn)
    while grid_get(grid, posn) != '#':
        under = move_down(grid, posn)
        if grid_get(grid, under) == '|' or grid_get(grid, under) == EMPTY_SPACE:
            return posn
        posn = move_left(grid, posn)
        if posn is None:
            return posn
    return posn

def find_right(grid, posn):
    under = move_down(grid, posn)
    if grid_get(grid, under) == '|' or grid_get(grid, under) == EMPTY_SPACE:
        posn = move_right(grid, posn)
    while grid_get(grid, posn) != '#':
        under = move_down(grid, posn)
        if grid_get(grid, under) == '|' or grid_get(grid, under) == EMPTY_SPACE:
            break
        posn = move_right(grid, posn)
        if posn is None:
            return posn
    return posn


def drip(grid, spring):
    parent = {}
    queue = [spring]
    while queue:
        posn = queue.pop()
        down = move_down(grid, posn)

        if down is None:
            continue

        if down and grid_get(grid, down) != "#" and grid_get(grid, down) != "~":
            grid_set(grid, down, '|')
            parent[down] = posn
            queue.append(down)
        else:
            right = find_right(grid, posn)
            left = find_left(grid, posn)
            if left is None or right is None:
                break
            if grid_get(grid, left) == '#' and grid_get(grid, right) == '#':
                fill_between(grid, left, right, "~")
                queue.append(parent[posn])
            else:
                fill_between(grid, left, right, "|")
                if grid_get(grid, left) == EMPTY_SPACE:
                    grid_set(grid, left, '|')
                    parent[left] = posn
                    queue.append(left)
                if grid_get(grid, right) == EMPTY_SPACE:
                    grid_set(grid, right, '|')
                    parent[right] = posn
                    queue.append(right)


def solve_a(grid, miny):
    "Solve first part of puzzle."
    soln = 0
    for y in range(miny, len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] in ['~', '|']:
                soln += 1
    return soln


def solve_b(grid, miny):
    "Solve second part of puzzle."
    soln = 0
    for y in range(miny, len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '~':
                soln += 1
    return soln


def main():
    "Main program."
    import sys
    veins = [parse_scan(ln) for ln in sys.stdin]
    grid, spring, miny, maxy = new_map(veins)
    drip(grid, spring)
    # print_grid(grid)
    print(solve_a(grid, miny))
    print(solve_b(grid, miny))



if __name__ == '__main__':
    main()
