"""
Advent of Code 2018
Day 2 ::
"""
import day02


def test_solveA():
    "Test solveA"
    data = ["abcdef", "bababc", "abbcde", "abcccd", "aabcdd", "abcdee", "ababab"]
    assert day02.solveA(data) == 12


def test_off_by_one():
    "Test off_by_one()"
    data = ['abcde', 'fghij', 'klmno', 'pqrst', 'fguij', 'axcye', 'wvxyz']
    assert day02.off_by_one(data) == ('fghij', 'fguij')


def test_common_letters():
    assert day02.common_letters('fghij', 'fguij') == 'fgij'


def test_solveB():
    data = ['abcde', 'fghij', 'klmno', 'pqrst', 'fguij', 'axcye', 'wvxyz']
    assert day02.solveB(data) == 'fgij'
