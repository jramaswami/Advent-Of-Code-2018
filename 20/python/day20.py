"""
Advent of Code 2018
Day 20: A Regular Map
"""
from collections import Counter, namedtuple
from math import inf

Posn = namedtuple('Posn', ['x', 'y'])

def move_north(grid, posn):
    grid[Posn(posn.x + 1, posn.y - 1)] = '#'
    grid[Posn(posn.x - 1, posn.y - 1)] = '#'
    grid[Posn(posn.x, posn.y - 1)] = '-'
    grid[Posn(posn.x, posn.y - 2)] = '.'
    return Posn(posn.x, posn.y - 2)

def move_south(grid, posn):
    grid[Posn(posn.x + 1, posn.y + 1)] = '#'
    grid[Posn(posn.x - 1, posn.y + 1)] = '#'
    grid[Posn(posn.x, posn.y + 1)] = '-'
    grid[Posn(posn.x, posn.y + 2)] = '.'
    return Posn(posn.x, posn.y)

def move_west(grid, posn):
    grid[Posn(posn.x - 1, posn.y + 1)] = '#'
    grid[Posn(posn.x - 1, posn.y - 1)] = '#'
    grid[Posn(posn.x - 1, posn.y)] = '|'
    grid[Posn(posn.x - 2, posn.y)] = '.'
    return Posn(posn.x - 2, posn.y)

def move_east(grid, posn):
    grid[Posn(posn.x + 1, posn.y + 1)] = '#'
    grid[Posn(posn.x + 1, posn.y - 1)] = '#'
    grid[Posn(posn.x + 1, posn.y)] = '|'
    grid[Posn(posn.x + 2, posn.y)] = '.'
    return Posn(posn.x + 2, posn.y)

def inbounds(grid, posn):
    return posn.x >= 0 and posn.y >= 0 and posn.x <= len(grid[0]) and posn.y <= len(grid)

def grid_string(grid):
    min_x = min_y = 1000000000
    max_x = max_y = -1000000000
    for posn in grid:
        min_x = min(posn.x, min_x)
        max_x = max(posn.x, max_x)
        min_y = min(posn.y, min_y)
        max_y = max(posn.y, max_y)

    print(min_x, max_x, min_y, max_y)

    grid0 = []
    for y in range(min_y, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            cell = grid.get(Posn(x, y), '?')
            row.append(cell)
        grid0.append(row)

    return "\n".join("".join(r) for r in grid0)


def new_grid(size):
    ht = 1 + (size * 2)
    wd = 1 + (size * 2)
    grid = [['?' for _ in range(wd)] for _ in range(ht)]
    grid[size][size] = 'X'
    return grid


def draw_map(regex, grid):
    "Draw the map for the given regex."
    parent = []
    stack = []
    posn = Posn(0, 0)
    grid[posn] = 'X'
    moves = {'N': move_north, 'S': move_south, 'E': move_east, 'W': move_west}
    for c in regex[1:-1]:
        print(c)
        if c == '(':
            break
        elif c in ['N', 'S', 'E', 'W']:
            move = moves[c]
            posn = move(grid, posn)
            print(posn)
    print(grid)
    print(grid_string(grid))

def do_move(move, level):
    print('\t'*level, 'm', move)

def do_branch(branch, level):
    index = 0
    options = []
    me = ''
    while index < len(branch):
        if branch[index] == '(':
            end_index = branch.rfind(')')
            for opt in do_branch(branch[index+1:end_index], level + 1):
                options.append(me + opt)
            index = end_index
            me = ''
            if end_index != len(branch) - 2:
                print('BOO', end_index, len(branch) - 2, level)
        elif branch[index] == '|':
            options.append(me)
            print('|', me, options)
            me = ''
        else:
            me = me + branch[index]
        index += 1
    if me:
        options.append(me)
        print('|', me, options)
    print('\t'*level, 'b', branch, options)
    return options


def main():
    "Main program."
    import sys
    regex = sys.stdin.read().strip()
    grid = {Posn(0, 0): 'X'}
    draw_map(regex, grid)


if __name__ == '__main__':
    main()
