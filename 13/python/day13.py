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
        self.dead = False

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
        self.cart_count = len(self.carts)

    def kill_carts(self, x, y):
        "Kill carts at x, y"
        body_count = 0
        for cart in self.carts:
            if cart.dead:
                continue
            if cart.x == x and cart.y == y:
                cart.dead = True
                body_count += 1
        self.mine_map[y][x] = self.clean_map[y][x]
        assert body_count == 2
        self.cart_count -= 2
        assert self.cart_count > 0
        assert self.cart_count % 2 == 1

    def detect_collision(self, cart0):
        "Detect collision."
        for cart1 in self.carts:
            if cart0.id == cart1.id:
                continue
            if cart1.dead:
                continue
            if cart0.x == cart1.x and cart0.y == cart1.y:
                return cart1
        return None

    def tick(self, explode=False):
        "Move forward one unit in time."
        for cart in self.carts:
            if explode and cart.dead:
                continue
            prev_x, prev_y = cart.x, cart.y
            cart.move()
            # update map with old symbol
            self.mine_map[prev_y][prev_x] = self.clean_map[prev_y][prev_x]
            # detect collision:
            if self.mine_map[cart.y][cart.x] in ['^', 'v', '>', '<']:
                if explode:
                    self.kill_carts(cart.x, cart.y)
                else:
                    self.mine_map[cart.y][cart.x] = 'X'
                    return (cart.x, cart.y)

            # update carts direction
            if not cart.dead:
                cart.update_direction(self.clean_map[cart.y][cart.x])
                self.mine_map[cart.y][cart.x] = cart.direction

            assert self.clean_map[cart.y][cart.x] in ['|', '-', '/', '\\', '+']
            if self.clean_map[cart.y][cart.x] == '|':
                assert cart.direction == '^' or cart.direction == 'v'
            if self.clean_map[cart.y][cart.x] == '-':
                assert cart.direction == '>' or cart.direction == '<'

        if explode:
            assert len([c for c in map_to_string(self.mine_map)
                        if c in ['v','^','>','<']]) == self.cart_count
            if self.cart_count == 1:
                survivor = [c for c in self.carts if not c.dead][0]
                return (survivor.x, survivor.y)

        self.carts.sort()

    def solve_a(self):
        "Solve first part of puzzle."
        while True:
            result = self.tick()
            if result:
                return result

    def solve_b(self):
        "Solve first part of puzzle."
        t = 0
        while True:
            t += 1
            result = self.tick(explode=True)
            assert self.cart_count % 2 == 1
            if result:
                return result

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

def main():
    "Main program."
    import sys
    input_lines = (sys.stdin.readlines())
    mine_map = MineMap(input_lines)
    print(mine_map.solve_a())
    mine_map = MineMap(input_lines)
    print(mine_map.solve_b())


if __name__ == '__main__':
    main()
