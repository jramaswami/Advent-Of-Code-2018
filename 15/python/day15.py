"""
Advent of Code 2018
Day 15: Beverage Bandits
"""

class Posn:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Posn({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x
        return self.y < other.y

    def __add__(self, other):
        return Posn(self.x + other.x, self.y + other.y)

    def manhattan_dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

class Unit:
    def __init__(self, posn, utype, uid, grid):
        self.hitpoints = 200
        self.attack_damage = 3
        self.posn = posn
        self.utype = utype
        self.uid = uid
        self.grid = grid
        if self.utype == 'E':
            self.enemy_type = 'G'
        else:
            self.enemy_type = 'E'

    def is_my_enemy(self, other):
        "Return true if other is an enemy."
        if isinstance(other, str):
            return self.enemy_type == other
        return other.utype == self.enemy_type

    def find_nearest_enemy_space(self):
        "Find the nearest enemy space."
        print(self, 'looking for nearest enemy space ...')
        enemy_spaces = []
        for enemy in [u for u in self.grid.units if self.is_my_enemy(u)]:
            for space in self.grid.neighbors(enemy.posn):
                if self.grid[space] == '.':
                    enemy_spaces.append((space.manhattan_dist(self.posn), space))
        if enemy_spaces:
            enemy_spaces.sort()
            print(self, 'found enemy spaces', enemy_spaces)
            return enemy_spaces[0][1]
        return None

    def find_next_step(self):
        "Find next step."
        for posn0 in self.grid.neighbors(self.posn):
            if self.is_my_enemy(self.grid[posn0]):
                return None

        print(self, 'looking for next step ...' )
        enemy_space = self.find_nearest_enemy_space()
        if enemy_space:
            steps = sorted((st.manhattan_dist(enemy_space), st)
                           for st in self.grid.neighbors(self.posn))
            print(self, 'my possible steps', steps)
            return steps[0][1]

    def move(self):
        next_step = self.find_next_step()
        if next_step:
            print(self, 'moving to', next_step)
            self.grid[self.posn] = '.'
            self.posn = next_step
            self.grid[self.posn] = self

    def die(self):
        self.grid[self.posn] = '.'
        self.grid.units.remove(self)

    def attack(self):
        print(self, 'looking for targets ...')
        enemies_in_range = []
        for posn in self.grid.neighbors(self.posn):
            nbr = self.grid[posn]
            if isinstance(nbr, Unit) and self.is_my_enemy(nbr):
                enemies_in_range.append(nbr)
        if enemies_in_range:
            enemies_in_range.sort()
            target = enemies_in_range[0]
            print(self, 'attacking target', target)
            target.hitpoints -= self.attack_damage
            if target.hitpoints <= 0:
                target.die()

    def __repr__(self):
        return "{}{}hp{}@{}".format(self.utype, self.uid, self.hitpoints, self.posn)

    def __lt__(self, other):
        if self.hitpoints == other.hitpoints:
            return self.posn < other.posn
        return self.hitpoints < other.hitpoints


class Grid:
    def __init__(self, input_lines):
        self.time = 0
        self.grid = []
        self.units = []
        unit_id = 0
        for y, line in enumerate(input_lines):
            line = line.strip()
            grid_row = []
            for x, char in enumerate(line):
                if char == 'E' or char == 'G':
                    self.units.append(Unit(Posn(x, y), char, unit_id, self))
                    unit_id += 1
                    grid_row.append(self.units[-1])
                else:
                    grid_row.append(char)
            self.grid.append(grid_row)
        self.wd = len(self.grid[0])
        self.ht = len(self.grid)

    def inbounds(self, posn):
        "Return True if x and y are in the grid."
        return posn.x >= 0 and posn.x < self.wd \
               and posn.y >= 0 and posn.y < self.ht

    def neighbors(self, posn):
        "Get four neighboring squares for x, y"
        offsets = [Posn(0, -1), Posn(-1, 0), Posn(1, 0), Posn(0, 1)]
        nbrs = []
        for delta in offsets:
            posn0 = posn + delta
            if self.inbounds(posn0):
                nbrs.append(posn0)
        return nbrs

    def tick(self):
        "Tick."
        self.time += 1
        print('Tick', self.time)
        for unit in self.units:
            unit.move()
            unit.attack()
        print(self.units)
        print('*****')


    def __getitem__(self, key):
        if isinstance(key, Posn):
            return self.grid[key.y][key.x]
        return self.grid[key]

    def __setitem__(self, key, value):
        if isinstance(key, Posn):
            self.grid[key.y][key.x] = value

    def __repr__(self):
        repr_rows = []
        for row in self.grid:
            repr_row = []
            for cell in row:
                if isinstance(cell, Unit):
                    repr_row.append(cell.utype)
                else:
                    repr_row.append(cell)
            repr_rows.append("".join(repr_row))
        return "\n".join(repr_rows)


def grid_from_file(file_name):
    "Get grid from a file."
    with open(file_name) as input_file:
        return Grid(input_file.readlines())




def solve_a():
    "Solve first part of puzzle."
    pass


def solve_b():
    "Solve second part of puzzle."
    pass


def main():
    "Main program."
    pass

if __name__ == '__main__':
    main()

