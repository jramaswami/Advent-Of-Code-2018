"""
Advent of Code 2018
Day 11: Chronal Charge
Tests
"""
import day11 as d11

def test_power_level():
    "Test power_level()"
    assert d11.power_level(3, 5, 8) == 4
    assert d11.power_level(122, 79, 57) == -5
    assert d11.power_level(217, 196, 39) == 0
    assert d11.power_level(101, 153, 71) == 4


def test_max_power():
    "Test max_power()"
    grid = d11.make_grid(18, 300)
    assert d11.max_power_square(grid, 3) == (33, 45, 29)
    grid = d11.make_grid(42, 300)
    assert d11.max_power_square(grid, 3) == (21, 61, 30)


def test_build_summed_area_table():
    "Test build_summed_area_table()"
    grid = [[3, 2, 1, 8],  [9, 11, 15, 0], [8, 4, 7, 6], [12, 7, 8, 3]]
    expected = [[3, 5, 6, 14], [12, 25, 41, 49], [20, 37, 60, 74], [32, 56, 87, 104]]
    assert d11.build_summed_area_table(grid) == expected

def test_query_summed_area_table():
    import random
    grid = [[3, 2, 1, 8],  [9, 11, 15, 0], [8, 4, 7, 6], [12, 7, 8, 3]]
    table = d11.build_summed_area_table(grid)
    assert d11.query_summed_area_table(table, 0, 0, len(grid)) == 104
    assert d11.query_summed_area_table(table, 1, 1, 3) == 61
    assert d11.query_summed_area_table(table, 0, 2, 2) == 8 + 4 + 12 + 7
    assert d11.query_summed_area_table(table, 1, 1, 2) == 11 + 15 + 4 + 7
    assert d11.query_summed_area_table(table, 1, 0, 3) == 2 + 1 + 8 + 11 + 15 + 0 + 4 + 7 + 6

