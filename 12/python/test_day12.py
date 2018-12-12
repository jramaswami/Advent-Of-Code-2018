"""
Advent of Code 2018
Day 12: Subterranean Sustainability
Tests
"""
from collections import deque
import day12 as d12

def test_parsing():
    "Test parsing."
    garden = d12.from_file('../test12.txt')
    assert garden.plants == deque(c for c in '#..#.#..##......###...###')

def test_states():
    "Test states."
    garden = d12.CaveGarden()
    states = ['#..#. => .', '..#.. => .', '..#.# => #', '##.#. => .',
              '.#... => #', '#.... => .', '##### => #', '.#.## => .',
              '#.#.. => .', '#.### => #', '.##.. => #', '##... => .',
              '#...# => #', '####. => #', '#.#.# => .', '#..## => .',
              '.#### => .', '...## => .', '..### => #', '.#..# => .',
              '##..# => #', '.#.#. => .', '..##. => .', '###.. => .',
              '###.# => #', '#.##. => #', '..... => .', '.##.# => #',
              '....# => .', '##.## => #', '...#. => #', '.###. => .']
    for state in states:
        garden.add_state(state)

    for state in states:
        current_state, expected_next_state = state.split(' => ')
        next_state = garden.get_next_state(current_state)
        assert next_state == expected_next_state
