"""
Advent of Code 2018
Day 20: A Regular Map
"""
from collections import Counter, namedtuple, deque
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

def get_options(branch):
    options = []
    start = 0
    index = 0
    pstack = []
    while index < len(branch):
        t = branch[index]
        if not pstack and t == '|':
            options.append(branch[start:index])
            start = index + 1
        elif t == '(':
            pstack.append('(')
        elif t == ')':
            pstack.pop()
        index += 1
    options.append(branch[start:index])
    assert not pstack
    assert options
    return options


def dfs(branch, path):
    index = 0
    queue = [path]
    while index < len(branch):
        new_queue = []
        path = queue.pop()
        if branch[index].isalpha():
            path += branch[index]
            new_queue.append(path)
        elif branch[index] == '$':
            new_queue.append(path)
            index += 1
        if branch[index] == '(':
            end_index = branch.rfind(')')
            for opts in get_options(branch[index+1:branch.rfind(')')]):
                dfs(branch, path)

            index = end_index
        queue = new_queue
        index += 1


def split_regex(regex):
    left_paren = regex.find('(')
    if left_paren >= 0:
        right_paren = regex.rfind(')')
        assert right_paren >= 0
        left = regex[0:left_paren]
        middle = regex[left_paren+1:right_paren]
        right = regex[right_paren+1:]
        return left, middle, right
    else:
        return regex, '', ''

def parse_regex(regex, tokens, parent, child):
    left, middle, right = split_regex
    tokens.append(left)
    if right:
        tokens.append(right)



def tokenize(chars: str) -> list:
    "Convert a string of characters into a list of tokens."
    chars = chars.replace('|)','|.)')
    chars = chars.replace('(', ' ( ')
    chars = chars.replace(')', ' ) ')
    chars = chars.replace('|', ' | ').split()
    return chars

def read_from_tokens(tokens: list):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)
    if token == '|':
        token = tokens.pop(0)

    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return token

def main():
    "Main program."
    import sys
    regex = sys.stdin.read().strip()
    grid = {Posn(0, 0): 'X'}
    draw_map(regex, grid)


if __name__ == '__main__':
    main()
