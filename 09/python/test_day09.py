"""
Advent of Code 2018
Day 9: Marble Mania
Tests
"""
import day09 as d9

def test_insert():
    "Test insertion into marble circle"
    marbles = d9.MarbleCircle()
    expected = [[0],
                [0, -1],
                [0, -2,  1],
                [0,  2,  1, -3],
                [0, -4,  2,  1,  3],
                [0,  4,  2, -5,  1,  3],
                [0,  4,  2,  5,  1, -6,  3],
                [0,  4,  2,  5,  1,  6,  3, -7],
                [0, -8,  4,  2,  5,  1,  6,  3,  7],
                [0,  8,  4, -9,  2,  5,  1,  6,  3,  7],
                [0,  8,  4,  9,  2,-10,  5,  1,  6,  3,  7],
                [0,  8,  4,  9,  2, 10,  5,-11,  1,  6,  3,  7],
                [0,  8,  4,  9,  2, 10,  5, 11,  1,-12,  6,  3,  7],
                [0,  8,  4,  9,  2, 10,  5, 11,  1, 12,  6,-13,  3,  7],
                [0,  8,  4,  9,  2, 10,  5, 11,  1, 12,  6, 13,  3,-14,  7],
                [0,  8,  4,  9,  2, 10,  5, 11,  1, 12,  6, 13,  3, 14,  7,-15],
                [0,-16,  8,  4,  9,  2, 10,  5, 11,  1, 12,  6, 13,  3, 14,  7, 15],
                [0, 16,  8,-17,  4,  9,  2, 10,  5, 11,  1, 12,  6, 13,  3, 14,  7, 15],
                [0, 16,  8, 17,  4,-18,  9,  2, 10,  5, 11,  1, 12,  6, 13,  3, 14,  7, 15],
                [0, 16,  8, 17,  4, 18,  9,-19,  2, 10,  5, 11,  1, 12,  6, 13,  3, 14,  7, 15],
                [0, 16,  8, 17,  4, 18,  9, 19,  2,-20, 10,  5, 11,  1, 12,  6, 13,  3, 14,  7, 15],
                [0, 16,  8, 17,  4, 18,  9, 19,  2, 20, 10,-21,  5, 11,  1, 12,  6, 13,  3, 14,  7, 15],
                [0, 16,  8, 17,  4, 18,  9, 19,  2, 20, 10, 21,  5,-22, 11,  1, 12,  6, 13,  3, 14,  7, 15]]
    for i in range(len(expected)):
        marbles.insert(i)
        assert expected[i] == [v for v in marbles]