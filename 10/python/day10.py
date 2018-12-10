"""
Advent of Code 2018
Day 10: The Stars Align
"""
from collections import namedtuple


Star = namedtuple("Star", ["x", "y", "dx", "dy"])
Grid = namedtuple("Grid", ["grid", "wd", "ht", "offx", "offy"])


def parse_star(input_string):
    "Parse input into a star."
    # position
    left_bracket = input_string.find("<")
    right_bracket = input_string.find(">")
    x, y = (int(i) for i in input_string[left_bracket + 1: right_bracket].split(','))
    left_bracket = input_string.find("<", right_bracket + 1)
    right_bracket = input_string.find(">", right_bracket + 1)
    dx, dy = (int(i) for i in input_string[left_bracket + 1: right_bracket].split(','))
    return Star(x, y, dx, dy)


def on_screen(star, tick, grid):
    "Return true if x/y is on grid."
    x = star.x + (tick * star.dx)
    y = star.y + (tick * star.dy)
    return (x >= -grid.offx and x <= grid.offx and
            y >= -grid.offy and y <= grid.offy)


def plot_star(star, tick, grid):
    "Put star on grid, if it is in view."
    if on_screen(star, tick, grid):
        x = star.x + (star.dx * tick) + grid.offx
        y = star.y + (star.dy * tick) + grid.offy
        grid.grid[y][x] = '#'
        return True
    return False


def print_grid(grid):
    "Print grid."
    for row in grid.grid:
        print("".join(row))
    print()


def solveA(stars):
    "Solve first part of puzzle."
    height = 17
    start_y = 8
    width = 181
    start_x = 90
    for tick in range(5):
        grid = Grid([['.' for _ in range(width)] for _ in range(height)],
                    width, height, start_x, start_y)
        result = [plot_star(star, tick, grid) for star in stars]
        if result:
            print_grid(grid)


def solveB():
    "Solve second part of puzzle."
    pass

def main():
    "Main program."
    import sys
    stars = [parse_star(l) for l in sys.stdin]
    solveA(stars)


if __name__ == '__main__':
    main()
