"""
Advent of Code 2018
Day 22: Mode Maze
"""
from collections import namedtuple
from math import inf
import heapq

State = namedtuple('State', ['time', 'equip', 'x', 'y'])

ROCKY = NEITHER = 0
WET = TORCH = 1
NARROW = CLIMBING = 2
TSTR = ['rocky', 'wet', 'narrow']
ESTR = ['neither', 'torch', 'climbing']


def neighborhood(cave, x0, y0):
    "Return neighbors."
    offsets = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    neighbors = []
    for dy, dx in offsets:
        x = x0 + dx
        y = y0 + dy
        if x >= 0 and x < len(cave[0]) \
        and y >= 0 and y <= len(cave):
            neighbors.append((x, y))
    return neighbors

def scan_cave(depth, target_x, target_y, ht, wd):
    cave = [[None for _ in range(ht)] for _ in range(wd)]
    for y in range(len(cave)):
        for x in range(len(cave[0])):
            g = 0
            if x == 0 and y == 0:
                g = 0
            elif x == target_x and y == target_y:
                g = 0
            elif y == 0:
                g = x * 16807
            elif x == 0:
                g = y * 48271
            else:
                g = cave[y][x-1] * cave[y-1][x]

            e = (g + depth) % 20183
            cave[y][x] = e

    for y in range(len(cave)):
        for x in range(len(cave[0])):
            cave[y][x] = cave[y][x] % 3

    return cave


def cave_to_string(cave, target_x, target_y):
    symbols = ['.','=','|']
    rows = []
    for y in range(len(cave)):
        row = []
        for x in range(len(cave[0])):
            if y == 0 and x == 0:
                row.append('M')
            elif x == target_x and y == target_y:
                row.append('T')
            else:
                row.append(symbols[cave[y][x]])
        rows.append("".join(row))
    return "\n".join(rows)


def other_valid_equipment(equip, terrain):
    other = [[None, 2, 1], # ROCKY
             [2, None, 0], # WET
             [1, 0, None]]  # NARROW
    equip0 = other[terrain][equip]
    assert equip0 != terrain
    return equip0

def find_path(cave, target_x, target_y):
    dist = {}
    init = (0, TORCH, 0, 0)
    pq = [init]
    dist[(0, 0, 0)] = 0
    while pq:
        # print('pq', pq)
        # print('dist', dist)
        time, equip, x, y = heapq.heappop(pq)
        terrain = cave[y][x]
        # print('curr status', time, ESTR[equip], (x, y), TSTR[terrain])
        if target_x == x and target_y == y:
            if equip == TORCH:
                return time
            else:
                heapq.heappush(pq, (time + 7, TORCH, x, y))
        neighbors = neighborhood(cave, x, y)

        # move with current equip
        for x0, y0 in neighbors:
            terrain0 = cave[y0][x0]
            # print('neighbor', (x0, y0), TSTR[terrain0])
            if terrain0 != equip:
                shortest = dist.get((x0, y0, equip), inf)
                if time + 1 <  shortest:
                    # print('adding neighbor', (x0, y0), TSTR[terrain0], 'time', time+1)
                    heapq.heappush(pq, (time + 1, equip, x0, y0))
                    dist[(x0, y0, equip)] = time + 1
                # else:
                    # print('neighbor', (x0, y0), TSTR[terrain0], 'has shorter time', shortest)

        # change equip
        equip0 = other_valid_equipment(equip, terrain)
        time0 = time + 7
        if time0 < dist.get((x, y, equip0), inf):
            # print('adding equip change', ESTR[equip0], (x, y), 'time', time0)
            heapq.heappush(pq, (time0, equip0, x, y))
            dist[(x, y, equip0)] = time0


def solve_a(cave, target_x, target_y):
    soln = 0
    for y in range(target_y+1):
        for x in range(target_x+1):
            soln += cave[y][x]
    return soln


def solve_b(cave, target_x, target_y):
    return find_path(cave, target_x, target_y)


def main():
    "Main program."
    # Puzzle input
    # depth, target_x, target_y = 510, 10, 10  # Test
    depth, target_x, target_y = 10689, 11, 722  # Puzzle Input
    # cave = scan_cave(depth, target_x, target_y, target_x + 1, target_y + 1)
    cave = scan_cave(depth, target_x, target_y, 1000, 1000)
    print(solve_a(cave, target_x, target_y))
    print(solve_b(cave, target_x, target_y))


if __name__ == '__main__':
    main()
