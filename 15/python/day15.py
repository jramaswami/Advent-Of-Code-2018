"""
Advent of Code 2018
Day 15: Beverage Bandits
"""
from collections import namedtuple
from math import inf


Posn = namedtuple('Posn', ['x', 'y'])


def manhattan_distance(posn0, posn1):
    "Manhattan distance."
    return abs(posn0.x - posn1.x) + abs(posn0.y - posn1.y)

def neighborhood(cave, posn):
    "Return neighbors."
    offsets = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    neighbors = []
    for dy, dx in offsets:
        x = posn.x + dx
        y = posn.y + dy
        if x >= 0 and x < len(cave[0]) \
        and y >= 0 and y <= len(cave) \
        and cave[y][x] != '#':
            neighbors.append(Posn(x, y))
    return neighbors


def is_enemy(me, other):
    "Is the other an enemy?"
    if other.isalpha():
        return me.isupper() != other.isupper()
    return False

def find_reachable_squares(cave, start):
    me = cave[start.y][start.x]
    reachables = set([])
    queue = neighborhood(cave, start)
    visited = set([start])
    dist = 0
    while queue:
        new_queue = []
        dist += 1
        for posn in queue:
            visited.add(posn)
            for neighbor in neighborhood(cave, posn):
                if neighbor in visited:
                    continue
                other = cave[neighbor.y][neighbor.x]
                if is_enemy(me, other):
                    reachables.add((dist, posn))
                elif other == '.':
                    new_queue.append(neighbor)
        queue = new_queue
    return reachables


def choose_reachable_square(reachable_squares):
    "Choose the best reachable square."
    min_dist = inf
    chosen_square = None
    for dist, posn in reachable_squares:
        if dist < min_dist:
            chosen_square = posn
            min_dist = dist
        if dist == min_dist:
            if posn.y < chosen_square.y:
                chosen_square = posn
            elif posn.y == chosen_square.y and posn.x < chosen_square.x:
                chosen_square = posn
    return chosen_square


def find_paths_to_target_square(cave, start, target_square):
    queue = [[start]]
    paths_to_target_square = []
    while queue and not paths_to_target_square:
        new_queue = []
        for path in queue:
            posn = path[-1]
            if posn == target_square:
                paths_to_target_square.append(path)
            else:
                for neighbor in neighborhood(cave, posn):
                    if neighbor in path:
                        continue
                    if cave[neighbor.y][neighbor.x] == '.':
                        path0 = list(path)
                        path0.append(neighbor)
                        new_queue.append(path0)
        queue = new_queue
    return paths_to_target_square


def choose_next_move_from_paths(paths_to_target_square):
    chosen_square = Posn(inf, inf)
    for path in paths_to_target_square:
        posn = path[1]
        if posn.y < chosen_square.y:
            chosen_square = posn
        elif posn.y == chosen_square.y and posn.x < chosen_square.x:
            chosen_square = posn
    return chosen_square


def get_best_paths(paths):
    best_paths = []
    best_posn = Posn(10000000, 1000000)
    for path in paths:
        reachable_square = path[-2]
        if reachable_square.y < best_posn.y:
            best_paths = [path]
            best_posn = reachable_square
        elif reachable_square.y == best_posn.y:
            if reachable_square.x == best_posn.x:
                best_paths.append(path)
            elif reachable_square.x < best_posn.x:
                best_paths = [path]
                best_posn = reachable_square
    return best_paths

def get_best_move(paths):
    "Return nearest move."
    best_mv = Posn(10000000, 1000000)
    for path in paths:
        mv = path[1]
        if mv.y < best_mv.y:
            best_mv = mv
        elif mv.y == best_mv.y:
            if mv.x < best_mv.x:
                best_mv = mv
    return best_mv


def get_next_move(cave, unit_posn):
    "Get the unit at given position's next move."
    paths = bfs(cave, unit_posn)
    if paths:
        best_paths = get_best_paths(paths)
        mv = get_best_move(best_paths)
        return mv


def parse_cave(input_lines):
    "Parse map of cave."
    cave = []
    elf_id = 0
    goblin_id = 0
    ord_a = ord('a')
    ord_A = ord('A')
    for line in input_lines:
        cave_row = []
        line = line.strip()
        for char in line:
            if char == 'E':
                elf = ord_A + elf_id
                elf_id += 1
                cave_row.append(chr(elf))
            elif char == 'G':
                goblin = ord_a + goblin_id
                goblin_id += 1
                cave_row.append(chr(goblin))
            else:
                cave_row.append(char)
        cave.append(cave_row)
    return cave


def cave_to_string(cave, no_ids=False):
    "Make cave a string."
    cave0 = []
    for row in cave:
        row0 = []
        for c in row:
            if no_ids:
                if c.isalpha():
                    if c.islower():
                        row0.append('G')
                    else:
                        row0.append('E')
                else:
                    row0.append(c)
            else:
                row0.append(c)
        cave0.append(row0)
    return "\n".join("".join(r) for r in cave0)


def move(cave, posn):
    me = cave[posn.y][posn.x]
    for neighbor in neighborhood(cave, posn):
        if is_enemy(me, cave[neighbor.y][neighbor.x]):
            print(me, 'engaged in combat @', posn)
            return

    print(me, 'moving')
    next_move = get_next_move(cave, posn)
    cave[posn.y][posn.x] = '.'
    cave[next_move.y][next_move.x] = me


def tick(cave):
    moved = set()
    for y in range(len(cave)):
        for x in range(len(cave[0])):
            if cave[y][x].isalpha():
                print(moved)
                if cave[y][x] not in moved:
                    moved.add(cave[y][x])
                    move(cave, Posn(x, y))
    print(cave_to_string(cave))


def cave_from_file(filename):
    "Get cave from a file."
    with open(filename) as inputf:
        cave = parse_cave(inputf.readlines())
        return cave


def main():
    "Main program."
    import sys
    cave = parse_cave(sys.stdin.readlines())
    print(cave_to_string(cave, no_ids=True))


if __name__ == '__main__':
    main()
