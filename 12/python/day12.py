"""
Advent of Code 2018
Day 12: Subterranean Sustainability
"""
from collections import deque

class CaveGarden:
    def __init__(self):
        self.plants = None
        self.states = ['' for _ in range(5 + (2**7))]
        self.states[1] = 'S'
        self.zero_index = 0

    def parse_plants(self, input_line):
        "Parse plants from input line."
        self.plants = deque(c for c in input_line.strip()[15:])

    def add_state(self, line):
        "Add to states."
        curr = 1
        for c in line[:5]:
            if c == '#':
                curr = 2 * curr
                self.states[curr] = '#'
            else:
                curr = 1 + (2 * curr)
                self.states[curr] = '.'
        c = line[-1]
        curr = 2 * curr
        self.states[curr] = c

    def parse_states(self, input_lines):
        "Parse states from list of input lines."
        for line in input_lines:
            line = line.strip()
            if not line:
                continue
            self.add_state(line)

    def get_next_state(self, current_state):
        "Return next state."
        curr = 1
        for c in current_state:
            if c == '#':
                curr = 2 * curr
            else:
                curr = 1 + (2 * curr)
        return self.states[2 * curr]

    def tick(self):
        "Move forward one unit of time."
        plants0 = deque(self.plants)
        # extend to make space for expansion
        while plants0[0] != '.' or plants0[1] != '.':
            plants0.appendleft('.')
            self.zero_index += 1
        while plants0[-2] != '.' or plants0[-1] != '.':
            plants0.append('.')

        for stx in range(len(self.plants) - 5):
            current_state = [self.plants[i] for i in range(stx, stx + 5)]
            next_state = self.get_next_state(current_state)
            if next_state == '':
                next_state = '.'
            plants0[stx+2] = next_state
        self.plants = plants0


def from_file(filename):
    "Read in data from file."
    garden = CaveGarden()
    with open(filename) as input_file:
        garden.parse_plants(input_file.readline())
        input_file.readline()
        garden.parse_states(input_file.readlines())
    return garden


def solve_a():
    "Solve first part of puzzle."
    pass


def main():
    "Main program."
    import sys
    garden = CaveGarden()
    garden.parse_plants(sys.stdin.readline())
    sys.stdin.readline()
    garden.parse_states(sys.stdin.readlines())


if __name__ == '__main__':
    main()
