"""
Advent of Code 2018
Day 16: Chronal Classification
Tests
"""
import day16 as d16

def test_operations_dict():
    "Make sure all operations appear in dict correctly."
    for name, fun in d16.OPERATIONS.items():
        assert name == fun.__name__


def test_parse_sample():
    "Test parse_sample()"
    input_lines = ["Before: [3, 2, 1, 1]\n", "9 2 1 2\n", "After:  [3, 2, 2, 1]\n"]
    actual = d16.parse_sample(input_lines)
    expected = d16.Sample((3, 2, 1, 1), d16.Instruction(9, 2, 1, 2), (3, 2, 2, 1))
    assert actual == expected


def test_find_valid_ops():
    "Test find_valid_ops()"
    input_lines = ["Before: [3, 2, 1, 1]\n", "9 2 1 2\n", "After:  [3, 2, 2, 1]\n"]
    sample = d16.parse_sample(input_lines)
    assert sorted(d16.find_valid_ops(sample)) == ['addi', 'mulr', 'seti']
