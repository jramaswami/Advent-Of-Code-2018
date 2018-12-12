"""
Advent of Code 2018
Day 11: Chronal Charge
"""
from tqdm import tqdm

def power_level(x, y, serial_number):
    "Return power level of given fuel cell."
    # Find the fuel cell's rack ID, which is its X coordinate plus 10.
    rack_id = x + 10
    # Begin with a power level of the rack ID times the Y coordinate.
    power = rack_id * y
    # Increase the power level by the value of the grid serial number
    # (your puzzle input).
    power += serial_number
    # Set the power level to itself multiplied by the rack ID.
    power *= rack_id
    # Keep only the hundreds digit of the power level (so 12345
    # becomes 3; numbers with no hundreds digit become 0).
    power = (power // 100) % 10
    # Subtract 5 from the power level.
    power -= 5
    return power


def square_power(x, y, grid, sq_sz):
    "Return power of square anchored at x, y"
    return sum(sum(grid[y][x:x+sq_sz]) for y in range(y, y+sq_sz))


def make_grid(serial_number, size):
    "Return grid."
    return [[power_level(x+1, y+1, serial_number)
             for x in range(size)]
             for y in range(size)]


def max_power_square(grid, square_size):
    "Return x, y of top left of max power square."
    max_x = max_y = max_pow = 0
    for x in range(0, len(grid) - square_size):
        for y in range(0, len(grid) - square_size):
            sq_pow = square_power(x, y, grid, square_size)
            if sq_pow > max_pow:
                max_x, max_y, max_pow = x, y, sq_pow
    return (max_x + 1, max_y + 1, max_pow)


def max_grid_value(grid):
    "Find the max value in the grid."
    max_x = max_y = max_pow = 0
    for y in range(len(grid)):
        for x in range(len(grid)):
            if grid[y][x] > max_pow:
                max_pow = grid[y][x]
                max_x = x
                max_y = y
    return max_x, max_y, max_pow


def get_or_zero(aux, x, y):
    "Return value at aux or zero if out of bounds."
    if x < 0 or y < 0:
        return 0
    else:
        return aux[y][x]


def build_summed_area_table(grid):
    "Build a summed area table."
    aux = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            aux[y][x] = (grid[y][x] +
                         get_or_zero(aux, x, y - 1) +
                         get_or_zero(aux, x - 1, y) -
                         get_or_zero(aux, x - 1, y - 1))
    return aux


def query_summed_area_table(aux, tlx, tly, size):
    "Query the summed area table for square rooted at (x,y) of given size."
    brx = tlx + size - 1
    bry = tly + size - 1
    result = aux[bry][brx]
    if tlx > 0:
        result -= aux[bry][tlx-1]
    if tly > 0:
        result -= aux[tly-1][brx]
    if tlx > 0 and tly > 0:
        result += aux[tly-1][tlx-1]
    return result


def solveB1(grid):
    "Solve second part of puzzle: summed area table."
    aux = build_summed_area_table(grid)
    max_x = max_y = max_pow = max_size = 0
    for square_size in tqdm(range(1, len(grid))):
        for x in range(0, len(grid) - square_size):
            for y in range(0, len(grid) - square_size):
                sq_pow = query_summed_area_table(aux, x, y, square_size)
                if sq_pow > max_pow:
                    max_x, max_y, max_pow, max_size = x, y, sq_pow, square_size
    return (max_x + 1, max_y + 1, max_pow, max_size)


def solveB0(grid):
    "Solve second part of puzzle: dynamic programming."
    grid0 = [[grid[y][x] for x in range(len(grid))] for y in range(len(grid))]
    max_x, max_y, max_pow = max_grid_value(grid0)
    max_sz = 1
    for off in tqdm(range(1, len(grid))):
        for y in range(len(grid) - off):
            for x in range(len(grid) - off):
                vert = [grid[y0][x+off] for y0 in range(y, y + off)]
                horiz = grid[y+off][x:x+off + 1]
                grid0[y][x] += sum(vert)
                grid0[y][x] += sum(horiz)
                if grid0[y][x] > max_pow:
                    max_x, max_y, max_pow, max_sz = x, y, grid0[y][x], off + 1
    return (max_x + 1, max_y + 1, max_pow, max_sz)


def solveB(grid):
    "Solve second part of puzzle: brute force."
    max_x = max_y = max_pow = max_size = 0
    for square_size in tqdm(range(1, len(grid))):
        x, y, pw = max_power_square(grid, square_size)
        if pw > max_pow:
            max_x, max_y, max_pow, max_size = x, y, pw, square_size
    return (max_x, max_y, max_pow, max_size)


def solveA(grid):
    "Solve first part of puzzle."
    return max_power_square(grid, 3)


def main():
    "Main program."
    grid = make_grid(6042, 300)
    print(solveA(grid))   # (x = 21, y = 61, power = 30)
    print(solveB1(grid))  # (x = 232, y = 251, size = 12, power = 119)


if __name__ == '__main__':
    main()
