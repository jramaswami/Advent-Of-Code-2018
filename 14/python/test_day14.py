"""
Advent of Code 2018
Day 14: Chocolate Charts
Tests
"""
import day14 as d14
from collections import namedtuple


TickResult = namedtuple('TickResult', ['board', 'elf1_pos', 'elf2_pos'])

def parse_test_data(input_string):
    "Parse the test data."
    board = []
    tokens = input_string.split()
    elf1 = elf2 = 0
    for index, token in enumerate(tokens):
        token = token.strip()
        if token[0] == "(":
            score = int(token[1])
            elf1 = index
        elif token[0] == '[':
            score = int(token[1])
            elf2 = index
        else:
            score = int(token)
        board.append(score)
    return TickResult(board, elf1, elf2)

def get_test_data_from_file(filename):
    "Get expected test data from file."
    with open(filename) as inp:
        expected = [parse_test_data(ln.strip()) for ln in inp]
        return expected

def test_tick():
    "Test tick."
    expected = get_test_data_from_file('../testdata14.txt')
    cc = d14.ChocolateChart()
    assert cc.score_board == expected[0].board
    assert cc.elf1_pos == expected[0].elf1_pos
    assert cc.elf2_pos == expected[0].elf2_pos
    for t in range(1, len(expected)):
        cc.tick()
        # print(expected[t].board, expected[t].elf1_pos, expected[t].elf2_pos)
        assert cc.score_board == expected[t].board
        assert cc.elf1_pos == expected[t].elf1_pos
        assert cc.elf2_pos == expected[t].elf2_pos

def test_solve_a():
    "Test solve_a."
    ticks = [9, 5, 18, 2018]
    expected_results = ['5158916779', '0124515891', '9251071085', '5941429882']
    for tick, exp in zip(ticks, expected_results):
        cc = d14.ChocolateChart()
        result = cc.solve_a(tick)
        # print(tick, cc.score_board, expected_results)
        assert result == exp

def test_solve_b():
    patterns = ['51589', '01245', '92510', '59414']
    expected = [9, 5, 18, 2018]
    for ptrn, exp in zip(patterns, expected):
        cc = d14.ChocolateChart()
        result = cc.solve_b(ptrn)
        assert result == exp



