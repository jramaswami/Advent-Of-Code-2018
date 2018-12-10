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


def plot_star(star, tick, grid):
    "Put star on grid, if it is in view."
    x = star.x + (star.dx * tick) + grid.offx
    y = star.y + (star.dy * tick) + grid.offy
    grid.grid[y][x] = '\u2588'


def print_grid(grid):
    "Print grid."
    for row in grid.grid:
        print("".join(row))
    print()


def stars_are_aligned(stars, tick):
    "Return true of stars are aligned."
    init_y = stars[0].y + (stars[0].dy * tick)
    for star in stars[1:]:
        delta = abs(init_y - (star.y + (star.dy * tick)))
        if delta > 9:
            return False
    return True


def solve(stars):
    "Solve both parts of the puzzle."
    tick = 1
    for tick in range(15000):
        if stars_are_aligned(stars, tick):
            min_y = min(star.y + (tick * star.dy) for star in stars)
            max_y = max(star.y + (tick * star.dy) for star in stars)
            min_x = min(star.x + (tick * star.dx) for star in stars)
            max_x = max(star.x + (tick * star.dx) for star in stars)
            height = 1 + max_y - min_y
            start_y = -min_y
            width = 1 + max_x - min_x
            start_x = -min_x
            grid = Grid([[' ' for _ in range(width)] for _ in range(height)],
                        width, height, start_x, start_y)
            for star in stars:
                plot_star(star, tick, grid)
            print_grid(grid)
            print('time', tick)
            return


def main():
    "Main program."
    import sys
    stars = [parse_star(l) for l in sys.stdin]
    solve(stars)


if __name__ == '__main__':
    main()
