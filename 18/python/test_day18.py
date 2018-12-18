"""
Advent of Code 2018
Day 18: Settlers of The North Pole
Tests
"""
import day18 as d18

def grid_from_file(filename):
    with open(filename) as infile:
        return [[c for c in ln.strip()] for ln in infile.readlines()]

def test_tick():
    grid = grid_from_file('../test/test18.txt')
    for t in range(1, 11):
        grid = d18.tick(grid)
        expected = grid_from_file("../test/tick{}.txt".format(t))
        print('expected')
        d18.print_grid(expected)
        print('actual')
        d18.print_grid(grid)
        assert grid == expected

    def test_solve_a():
        grid = grid_from_file('../test/test18.txt')
        assert d18.solve_a(grid) == 1147
        grid = grid_from_file('../input18.txt')
        assert d18.solve_a(grid) == 511000

