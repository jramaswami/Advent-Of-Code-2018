"""
Advent of Code 2018
Day 22: Mode Maze
Tests
"""
import day22 as d22

def test_scan_cave():
    with open('../test_cave.txt') as infile:
        expected = infile.read().strip()
    c = d22.scan_cave(510, 10, 10, 16, 16)
    # print('expected')
    # print(expected)
    # print('actual')
    # print(d22.cave_to_string(c, 10, 10))
    assert d22.cave_to_string(c, 10, 10) == expected

def test_solve_a():
    c = d22.scan_cave(510, 10, 10, 16, 16)
    assert d22.solve_a(c, 10, 10) == 114
    c = d22.scan_cave(10689, 11, 722, 1000, 1000)
    assert d22.solve_a(c, 11, 722) == 8575

def test_solve_b():
    c = d22.scan_cave(510, 10, 10, 20, 20)
    assert d22.solve_b(c, 10, 10) == 45
    c = d22.scan_cave(10689, 11, 722, 1000, 1000)
    assert d22.solve_b(c, 11, 722) == 999
