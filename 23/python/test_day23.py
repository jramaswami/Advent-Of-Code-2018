"""
Advent of Code 2018
Day 23: Experimental Emergency Teleportation
Tests
"""
import day23 as d23
from operator import attrgetter

def test_manhattan_distance():
    "Test manhattan distance"
    nanobot0 = d23.Nanobot(d23.Posn(0, 0, 0), 4)
    assert d23.manhattan_distance(nanobot0, d23.Nanobot(d23.Posn(0, 0, 0), 4)) == 0
    assert d23.manhattan_distance(nanobot0, d23.Nanobot(d23.Posn(1, 0, 0), 1)) == 1
    assert d23.manhattan_distance(nanobot0, d23.Nanobot(d23.Posn(4, 0, 0), 3)) == 4
    assert d23.manhattan_distance(nanobot0, d23.Nanobot(d23.Posn(0, 2, 0), 1)) == 2
    assert d23.manhattan_distance(nanobot0, d23.Nanobot(d23.Posn(0, 5, 0), 3)) == 5
    assert d23.manhattan_distance(nanobot0, d23.Nanobot(d23.Posn(0, 0, 3), 1)) == 3
    assert d23.manhattan_distance(nanobot0, d23.Nanobot(d23.Posn(1, 1, 1), 1)) == 3
    assert d23.manhattan_distance(nanobot0, d23.Nanobot(d23.Posn(1, 1, 2), 1)) == 4
    assert d23.manhattan_distance(nanobot0, d23.Nanobot(d23.Posn(1, 3, 1), 1)) == 5

def test_in_range():
    "Test in_range()"
    nanobot0 = d23.Nanobot(d23.Posn(0, 0, 0), 4)
    assert d23.in_range(nanobot0, d23.Nanobot(d23.Posn(0, 0, 0), 4))
    assert d23.in_range(nanobot0, d23.Nanobot(d23.Posn(1, 0, 0), 1))
    assert d23.in_range(nanobot0, d23.Nanobot(d23.Posn(4, 0, 0), 3))
    assert d23.in_range(nanobot0, d23.Nanobot(d23.Posn(0, 2, 0), 1))
    assert not d23.in_range(nanobot0, d23.Nanobot(d23.Posn(0, 5, 0), 3))
    assert d23.in_range(nanobot0, d23.Nanobot(d23.Posn(0, 0, 3), 1))
    assert d23.in_range(nanobot0, d23.Nanobot(d23.Posn(1, 1, 1), 1))
    assert d23.in_range(nanobot0, d23.Nanobot(d23.Posn(1, 1, 2), 1))
    assert not d23.in_range(nanobot0, d23.Nanobot(d23.Posn(1, 3, 1), 1))


def test_solve_a():
    "Test solve_a()"
    with open('../test23a.txt') as infile:
        nanobots = [d23.parse_nanobot(ln) for ln in infile.readlines()]
    assert d23.solve_a(nanobots) == 7
    with open('../input23.txt') as infile:
        nanobots = [d23.parse_nanobot(ln) for ln in infile.readlines()]
    assert d23.solve_a(nanobots) == 588


def test_solve_b():
    "Test solve_b()"
    with open('../test23b.txt') as infile:
        nanobots = [d23.parse_nanobot(ln) for ln in infile.readlines()]
    assert d23.solve_b(nanobots) == 36
    with open('../input23.txt') as infile:
        nanobots = [d23.parse_nanobot(ln) for ln in infile.readlines()]
    assert d23.solve_b(nanobots) == 111227643



