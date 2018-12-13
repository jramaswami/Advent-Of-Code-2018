"""
Advent of Code
Day 13: Mine Cart Madness
"""
from itertools import count
from collections import namedtuple

Posn = namedtuple('Posn', ['x', 'y'])

LEFT = 0
STRAIGHT = 1
RIGHT = 2

TURNS = {'>': ['^', '>', 'v'], '<': ['v', '<', '^'],
         'v': ['>', 'v', '<'], '^': ['<', '^', '>']}

OFFSETS = {'>': Posn(1, 0), '<': Posn(-1, 0),
           'v': Posn(0, 1), '^': Posn(0, -1)}

CURVES = {'/': {'^': '>', 'v': '<', '>': '^', '<': 'v'},
          '\\': {'^': '<', 'v': '>', '<': '^', '>': 'v'}}

class Cart:
    "Cart"
    def __init__(self, cart_id, x, y, direction):
        self.id = cart_id
        self.x = x
        self.y = y
        self.direction = direction
        self.curr_turn = LEFT

    def turn(self):
        "Turn"
        self.direction = TURNS[self.direction][self.curr_turn]
        self.curr_turn = next_turn(self.curr_turn)

    def move(self):
        off = OFFSETS[self.direction]
        self.x += off.x
        self.y += off.y

    def update_direction(self, map_cell):
        # Curve
        if map_cell == '\\' or map_cell == '/':
            self.direction = CURVES[map_cell][self.direction]
        elif map_cell == '+':
            self.turn()

    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x
        return self.y < other.y

    def __repr__(self):
        return "{}: {} ({}, {})".format(self.id, self.direction, self.x, self.y)


class MineMap:
    def __init__(self, input_lines):
        "Parse map from lines of input."
        self.mine_map = [[c for c in line.rstrip()] for line in input_lines]
        self.carts = []
        cart_id = count()
        self.clean_map = []
        for y, row in enumerate(self.mine_map):
            clean_row = []
            for x, char in enumerate(row):
                if char in ['<', '>', 'v', '^']:
                    self.carts.append(Cart(next(cart_id), x, y, char))
                    if char == '<' or char == '>':
                        clean_row.append('-')
                    else:
                        clean_row.append('|')
                else:
                    clean_row.append(char)
            self.clean_map.append(clean_row)
        self.carts.sort()

    def tick(self):
        "Move forward one unit in time."
        for cart in self.carts:
            prev_x, prev_y = cart.x, cart.y
            cart.move()
            # update map with old symbol
            self.mine_map[prev_y][prev_x] = self.clean_map[prev_y][prev_x]
            # detect collision:
            if self.mine_map[cart.y][cart.x] in ['^', 'v', '>', '<']:
                self.mine_map[cart.y][cart.x] = 'X'
                return (cart.x, cart.y)
            # update carts direction
            cart.update_direction(self.clean_map[cart.y][cart.x])
            self.mine_map[cart.y][cart.x] = cart.direction

            assert self.clean_map[cart.y][cart.x] in ['|', '-', '/', '\\', '+']
            if self.clean_map[cart.y][cart.x] == '|':
                assert cart.direction == '^' or cart.direction == 'v'
            if self.clean_map[cart.y][cart.x] == '-':
                assert cart.direction == '>' or cart.direction == '<'

        self.carts.sort()


    def __repr__(self):
        return "{}\n{}\n{}".format(map_to_string(self.mine_map),
                                   map_to_string(self.clean_map),
                                   repr(self.carts))


def next_turn(curr_turn):
    "Return the next turn a cart will take."
    if curr_turn == 2:
        return 0
    return curr_turn + 1


def map_to_string(mine_map):
    "Map to string."
    return "\n".join("".join(row) for row in mine_map)


def solve_a(mine_map):
    "Solve first part of puzzle."
    tick = 0
    while True:
        tick += 1
        result = mine_map.tick()
        if result:
            return result


def solve_b():
    "Solve second part of puzzle."
    pass


def main():
    "Main program."
    import sys
    mine_map = MineMap(sys.stdin.readlines())
    print(solve_a(mine_map))
    # print(solve_b())


if __name__ == '__main__':
    main()
