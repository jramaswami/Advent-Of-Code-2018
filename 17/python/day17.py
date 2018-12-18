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

def fill(grid, posn):
    queue = [posn]
    while queue:
        # print('Q', queue)
        posn = queue.pop()
        my_down_points = [posn]
        posn = move_down(grid, posn)
        while posn:
            cell = grid_get(grid, posn)
            if cell == '~':
                break
            if cell == '#':
                break
            grid_set(grid, posn, '~')
            my_down_points.append(posn)
            posn = move_down(grid, posn)

        if not posn:
            continue

        right_escape = left_escape = False

        while not (right_escape or left_escape) and my_down_points:
            # print_grid(grid)
            # print(my_down_points)
            posn = my_down_points.pop()
            posn0 = move_left(grid, posn)
            while posn0:
                cell = grid_get(grid, posn0)
                if cell == '#':
                    break
                grid_set(grid, posn0, '~')
                if grid_get(grid, move_down(grid, posn0)) == EMPTY_SPACE:
                    queue.append(posn0)
                    # fill(grid, posn0)
                    left_escape = True
                    break
                posn0 = move_left(grid, posn0)

            posn0 = move_right(grid, posn)
            while posn0:
                cell = grid_get(grid, posn0)
                if cell == '#':
                    break
                grid_set(grid, posn0, '~')
                if grid_get(grid, move_down(grid, posn0)) == EMPTY_SPACE:
                    queue.append(posn0)
                    # fill(grid, posn0)
                    right_escape = True
                    break
                posn0 = move_right(grid, posn0)

        # print_grid(grid)

    print_grid(grid)

def solve_a(veins):
    "Solve first part of puzzle."
    grid, spring = new_map(veins)
    fill(grid, spring)
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
