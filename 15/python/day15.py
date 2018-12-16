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


def is_elf(me):
    return me.isupper()


def is_enemy(me, other):
    "Is the other an enemy?"
    if other.isalpha():
        return me.isupper() != other.isupper()
    return False

def print_visited(cave, visited, me):
    rows = []
    for y in range(len(cave)):
        row = []
        for x in range(len(cave[0])):
            if Posn(x, y) in visited:
                row.append(me)
            else:
                row.append(cave[y][x])
        rows.append("".join(row))
    print("\n".join(rows))
    print()



def find_reachable_squares(cave, start):
    me = cave[start.y][start.x]
    # print(me, 'finding reachable squares')
    reachables = set([])
    queue = set([n for n in neighborhood(cave, start) if cave[n.y][n.x] == '.'])
    visited = set([start])
    dist = 0
    while queue:
        # print_visited(cave, visited, me)
        new_queue = set([])
        dist += 1
        for posn in queue:
            visited.add(posn)
            for neighbor in neighborhood(cave, posn):
                if neighbor not in visited:
                    other = cave[neighbor.y][neighbor.x]
                    if is_enemy(me, other):
                        reachables.add((dist, posn))
                    elif other == '.':
                        new_queue.add(neighbor)
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


def find_distance_between(cave, start, target):
    me = cave[start.y][start.y]
    # print('find distance between', start, target)
    if start == target:
        return 0
    queue = set([n for n in neighborhood(cave, start) if cave[n.y][n.x] == '.'])
    visited = set([start])
    dist = 0
    while queue:
        # print(queue)
        # print_visited(cave, visited, 'x')
        new_queue = set([])
        dist += 1
        for posn in queue:
            visited.add(posn)
            for neighbor in neighborhood(cave, posn):
                if neighbor not in visited:
                    if posn == target:
                        return dist
                    other = cave[neighbor.y][neighbor.x]
                    if other == '.':
                        new_queue.add(neighbor)
            queue = new_queue
    return inf


def choose_next_move(cave, start, target_square):
    # print('choose next move', start, target_square)
    min_dist = inf
    chosen_square = Posn(inf, inf)
    for posn in neighborhood(cave, start):
        if cave[posn.y][posn.x] == '.':
            dist = find_distance_between(cave, posn, target_square)
            # print('dist', dist, posn)
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
        # print(queue)
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


def parse_cave(input_lines):
    "Parse map of cave."
    cave = []
    elf_id = 0
    goblin_id = 0
    ord_a = ord('a')
    ord_A = ord('A')
    hitpoints = {}
    for line in input_lines:
        cave_row = []
        line = line.strip()
        for char in line:
            if char == 'E':
                elf = ord_A + elf_id
                elf_id += 1
                cave_row.append(chr(elf))
                hitpoints[chr(elf)] = 200
            elif char == 'G':
                goblin = ord_a + goblin_id
                goblin_id += 1
                cave_row.append(chr(goblin))
                hitpoints[chr(goblin)] = 200
            else:
                cave_row.append(char)
        cave.append(cave_row)
    return cave, hitpoints


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


def get_next_move(cave, unit_posn):
    me = cave[unit_posn.y][unit_posn.x]
    next_move = None
    reachable_squares = find_reachable_squares(cave, unit_posn)
    # print(me, 'reachable squares', reachable_squares)
    if reachable_squares:
        # print(me, 'choosing reachable squares')
        target_square = choose_reachable_square(reachable_squares)
        # print(me, 'target square', target_square)
        # print(me, 'finding path to chosen square')
        # paths_to_target_square = find_paths_to_target_square(cave, unit_posn, target_square)
        # print(me, 'choosing next move')
        # next_move = choose_next_move_from_paths(paths_to_target_square)
        next_move = choose_next_move(cave, unit_posn, target_square)
    return next_move


def move(cave, posn):
    me = cave[posn.y][posn.x]
    for neighbor in neighborhood(cave, posn):
        if is_enemy(me, cave[neighbor.y][neighbor.x]):
            return

    next_move = get_next_move(cave, posn)
    if next_move:
        # print(me, 'moving from', posn, 'to', next_move)
        cave[posn.y][posn.x] = '.'
        cave[next_move.y][next_move.x] = me
        return next_move


def choose_enemy_to_attack(cave, hitpoints, targets):
    chosen_enemy = Posn(inf, inf)
    chosen_enemy_hp = inf
    for posn in targets:
        enemy_id = cave[posn.y][posn.x]
        if hitpoints[enemy_id] < chosen_enemy_hp:
            chosen_enemy_hp = hitpoints[enemy_id]
            chosen_enemy = posn
        elif hitpoints[enemy_id] == chosen_enemy_hp:
            if posn.y < chosen_enemy.y:
                chosen_enemy = posn
            elif posn.y == chosen_enemy.y and posn.x < chosen_enemy.x:
                chosen_enemy = posn
    return chosen_enemy


def attack(cave, hitpoints, posn, elf_attack_points=3):
    me = cave[posn.y][posn.x]
    enemy_posns = [p for p in neighborhood(cave, posn) if is_enemy(me, cave[p.y][p.x])]
    if enemy_posns:
        target = choose_enemy_to_attack(cave, hitpoints, enemy_posns)
        target_id = cave[target.y][target.x]
        if is_elf(me):
            hitpoints[target_id] -= elf_attack_points
        else:
            hitpoints[target_id] -= 3
        # print(me, posn, 'attacking', target_id, '@', target, 'hp dn to', hitpoints[target_id])
        if hitpoints[target_id] <= 0:
            # print(target_id, 'has died')
            cave[target.y][target.x] = '.'


def tick_to_string(cave, hitpoints):
    cave0 = []
    for row in cave:
        row0 = []
        units_in_row = []
        for c in row:
            if c.isalpha():
                units_in_row.append(c)
                if c.islower():
                    row0.append('G')
                else:
                    row0.append('E')
            else:
                row0.append(c)
        cave_string = "".join(row0)
        if units_in_row:
            unit_strings = []
            for unit in units_in_row:
                if unit.islower():
                    utype = 'G'
                else:
                    utype = 'E'
                hp = hitpoints[unit]
                unit_strings.append("{}({})".format(utype, hp))
            hp_status = ", ".join(unit_strings)
            cave_string = cave_string + '   ' + hp_status
        cave0.append(cave_string)
    return "\n".join(cave0)


def enemies_still_alive(hitpoints, me):
    for other, hp in hitpoints.items():
        if hp > 0 and is_enemy(me, other):
            return True
    return False


def tick(cave, hitpoints, elf_attack_points=3):
    # print(hitpoints)
    completed_turn = set()
    for y in range(len(cave)):
        for x in range(len(cave[0])):
            if cave[y][x].isalpha():
                unit_id = cave[y][x]
                if unit_id not in completed_turn:
                    # print('action', unit_id)
                    completed_turn.add(unit_id)
                    posn0 = move(cave, Posn(x, y))

                    if not enemies_still_alive(hitpoints, unit_id):
                        return False

                    if posn0:
                        # print(unit_id, 'posn0', posn0)
                        attack(cave, hitpoints, posn0, elf_attack_points)
                    else:
                        attack(cave, hitpoints, Posn(x, y), elf_attack_points)
    return True


def is_victory(hitpoints):
    elves = sum(hp for uid, hp in hitpoints.items() if uid.isupper() and hp > 0)
    goblins = sum(hp for uid, hp in hitpoints.items() if uid.islower() and hp > 0)
    if elves <= 0:
        return ('G', goblins)
    elif goblins <= 0:
        return ('E', elves)
    return None


def solve_a(cave, hitpoints, elf_attack_points=3):
    print('Elf attack points', elf_attack_points)
    time = 0
    victory = is_victory(hitpoints)
    # print('init')
    # print(cave_to_string(cave))
    full_round = True
    while not victory:
        time += 1
        # print('Tick', time)
        full_round = tick(cave, hitpoints, elf_attack_points)
        # print(tick_to_string(cave, hitpoints))
        # print(cave_to_string(cave))
        # print(hitpoints)
        victory = is_victory(hitpoints)
    # print('victory', victory, 'time', time, 'full round', full_round)
    # print(tick_to_string(cave, hitpoints))
    if not full_round:
        time -= 1
    return victory[1] * time


def flawless_victory(hitpoints):
    for unit, hp in hitpoints.items():
        if is_elf(unit) and hp <= 0:
            return False
    return True


def solve_b(cave, hitpoints):
    import copy
    elf_attack_points = 4
    while True:
        cave0 = copy.deepcopy(cave)
        hitpoints0 = copy.deepcopy(hitpoints)
        score = solve_a(cave0, hitpoints0, elf_attack_points)
        if flawless_victory(hitpoints0):
            return score
        elf_attack_points += 1


def cave_from_file(filename):
    "Get cave from a file."
    with open(filename) as inputf:
        cave = parse_cave(inputf.readlines())
        return cave


def main():
    "Main program."
    import sys
    cave, hp = parse_cave(sys.stdin.readlines())
    # print(solve_a(cave, hp))
    print(solve_b(cave, hp))


if __name__ == '__main__':
    main()
