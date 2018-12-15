"""
Advent of Code 2018
Day 15: Beverage Bandits
"""

class Unit:
    def __init__(self, x, y, utype, uid, grid):
        self.x = x
        self.y = y
        self.utype = utype
        self.uid = uid
        self.grid = grid

    def find_nearest_enemy(self):
        "Do a bfs search to determine where unit is going."
        my_enemy = enemy(self.utype)
        queue = [[n] for n in self.grid.neighbors(self.x, self.y)]
        enemy_paths = []
        while queue and not enemy_paths:
            new_queue = []
            for path in queue:
                print(path)
                x, y = path[-1]
                for x0, y0 in self.grid.neighbors(x, y):
                    if (x0, y0) in path:
                        continue
                    new_path = list(path)
                    if self.grid[x0][y0] == my_enemy:
                        enemy_paths.append(path)
                    elif self.grid[x0][y0] == '.':
                        new_path.append((x0, y0))
                        print('enqueueing', new_path)
                        new_queue.append(new_path)
                queue = new_queue
        return enemy_paths

    def __repr__(self):
        return "{}{}@({}, {})".format(self.utype, self.uid, self.x, self.y)


class Grid:
    def __init__(self, input_lines):
        self.grid = []
        self.units = []
        unit_id = 0
        for y, line in enumerate(input_lines):
            line = line.strip()
            grid_row = []
            for x, char in enumerate(line):
                if char == 'E':
                    self.units.append(Unit(x, y, char, unit_id, self))
                    unit_id += 1
                grid_row.append(char)
            self.grid.append(grid_row)
        self.wd = len(self.grid)
        self.ht = len(self.grid[0])

    def inbounds(self, x, y):
        "Return True if x and y are in the grid."
        return x >= 0 and x < self.wd and y >= 0 and y < self.ht

    def neighbors(self, x, y):
        "Get four neighboring squares for x, y"
        offsets = [(0, -1), (-1, 0), (1, 0), (0, 1)]
        return [(x + dx, y + dy)
                for dx, dy in offsets
                if self.inbounds(x + dx, y + dy)]

    def __getitem__(self, index):
        return self.grid[index]

    def __repr__(self):
        return "\n".join("".join(row) for row in self.grid)


def grid_from_file(file_name):
    "Get grid from a file."
    with open(file_name) as input_file:
        return Grid(input_file.readlines())



def enemy(unit):
    "Return enemy of unit."
    if unit == 'E':
        return 'G'
    elif unit == 'G':
        return 'E'




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

