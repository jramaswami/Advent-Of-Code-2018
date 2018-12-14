"""
Advent of Code 2018
Day 14: Chocolate Charts
"""
from collections import deque

class ChocolateChart:
    def __init__(self):
        self.score_board = [3, 7]
        self.elf1_pos = 0
        self.elf2_pos = 1
        self.previous_recipes = 0
        self.search_queue = deque([3, 7])
        self.pattern_matching = False

    def tick(self):
        "Move forward one unit in time."
        elf1_score = self.score_board[self.elf1_pos]
        elf2_score = self.score_board[self.elf2_pos]
        new_scores = [int(i) for i in str(elf1_score + elf2_score)]
        self.score_board.extend(new_scores)
        if self.pattern_matching:
            self.search_queue.extend(new_scores)
        elf1_moves = elf1_score + 1
        elf2_moves = elf2_score + 1
        self.elf1_pos = self.elf1_pos + elf1_moves
        self.elf2_pos = self.elf2_pos + elf2_moves
        self.elf1_pos = (self.elf1_pos % len(self.score_board))
        self.elf2_pos = (self.elf2_pos % len(self.score_board))

    def solve_a(self, limit):
        "Solve first part of puzzle."
        while len(self.score_board) < (limit + 10 + 1):
            self.tick()
        return "".join(str(i) for i in self.score_board[limit:limit+10])

    def match(self, pattern):
        "Match."
        for index, number in enumerate(pattern):
            if number != self.search_queue[index]:
                return False
        return True

    def solve_b(self, pattern):
        "Solve second part of puzzle."
        import sys
        self.pattern_matching = True
        pattern0 = [int(i) for i in pattern]
        ticks = 0
        while True:
            self.tick()
            ticks += 1
            while len(self.search_queue) >= len(pattern0):
                # print('searching', self.search_queue)
                if self.match(pattern0):
                    return self.previous_recipes
                self.previous_recipes += 1
                self.search_queue.popleft()
            # if ticks % 100000 == 0:
                # print('.', end='')
            #     sys.stdout.flush()

def main():
    "Main program."
    cc = ChocolateChart()
    print(cc.solve_a(323081))
    cc = ChocolateChart()
    print(cc.solve_b('323081'))

if __name__ == '__main__':
    main()
