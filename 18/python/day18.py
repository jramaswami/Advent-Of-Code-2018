"""
Advent of Code 2018
Day 18: Settlers of The North Pole
"""
from collections import namedtuple, Counter

Posn = namedtuple('Posn', ['x', 'y'])

def moore_neighborhood(grid, posn):
    "Return moore neighborhood"
    neighborhood = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            x0 = posn.x + dx
            y0 = posn.y + dy
            if x0 >= 0 and y0 >= 0 and y0 < len(grid) and x0 < len(grid[0]):
                neighborhood.append(Posn(x0, y0))
    return neighborhood


def grid_get(grid, posn):
    "Get char from grid"
    return grid[posn.y][posn.x]


def grid_set(grid, posn, cell):
    "Set char on grid"
    grid[posn.y][posn.x] = cell


def print_grid(grid):
    "Print grid"
    print("\n".join("".join(r) for r in grid))


def transform(grid, posn):
    "What will cell be next?"
    # An open acre will become filled with trees if three or more
    # adjacent acres contained trees. Otherwise, nothing happens.
    neighbors = moore_neighborhood(grid, posn)
    cntr = Counter([grid_get(grid, n) for n in neighbors])
    cell = grid_get(grid, posn)
    if cell == '.':
        if cntr['|'] >= 3:
            return '|'
    # An acre filled with trees will become a lumberyard if three or more
    # adjacent acres were lumberyards. Otherwise, nothing happens.
    elif cell == '|':
        if cntr['#'] >= 3:
            return '#'
    # An acre containing a lumberyard will remain a lumberyard if it was
    # adjacent to at least one other lumberyard and at least one acre
    # containing trees. Otherwise, it becomes open.
    elif cell == '#':
        if cntr['#'] < 1 or cntr['|'] < 1:
            return '.'
    return cell


def tick(grid):
    "Make on tick of grid"
    grid0 = [['.' for _ in range(len(grid[0]))] for _ in range(len(grid))]
    for y in range(len(grid)):
        for x in range(len(grid)):
            posn = Posn(x, y)
            grid_set(grid0, posn, transform(grid, posn))
    return grid0


def grid_to_string(grid):
    return "".join("".join(r) for r in grid)

def count_resources(grid):
    cntr = {'|': 0, '.': 0, '#': 0}
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            cell = grid_get(grid, Posn(x, y))
            cntr[cell] += 1
    return cntr

def solve_b(grid):
    "Solve second part of puzzle."
    grids = {}
    # A cycle starts at tick 513, its period is 28
    # (1_000_000_000 - 513) % 28 = 524
    # So 1_000_000_000 minutes has same configuration as 524
    # Looking at configuration 524 gives resources as 194934 ('|': 613, '#': 318)
    cycle_start = 0
    period = 0
    for t in range(1, 600):
        grid = tick(grid)
        gstr = grid_to_string(grid)
        if gstr in grids:
            cycle_start = grids[gstr]
            period = t - cycle_start
            # print('Cycle start at', grids[gstr], 'with a period of', period)
            break
        grids[gstr] = t

    congruent_grid = ((1000000000 - cycle_start)) % period + cycle_start
    # print('Grid 1000000000 is congruent to grid', congruent_grid)
    for gstr, time in grids.items():
        if time == congruent_grid:
            cntr = Counter(gstr)
            return cntr['|'] * cntr['#']

def solve_a(grid):
    "Solve first part of puzzle."
    for _ in range(10):
        grid = tick(grid)
    cntr = count_resources(grid)
    return cntr['|'] * cntr['#']

def main():
    "Main program."
    import sys
    grid = [[c for c in ln.strip()] for ln in sys.stdin]
    print(solve_a(grid))
    print(solve_b(grid))

if __name__ == '__main__':
    main()