"""
Advent of Code
Day 13: Mine Cart Madness
"""
import day13 as d13

def test_turns():
    "Test turns."
    cart = d13.Cart(0, 0, 0, '>')
    assert cart.curr_turn == d13.LEFT
    cart.turn()
    assert cart.direction == '^'
    assert cart.curr_turn == d13.STRAIGHT
    cart.turn()
    assert cart.direction == '^'
    assert cart.curr_turn == d13.RIGHT
    cart.turn()
    assert cart.direction == '>'
    assert cart.curr_turn == d13.LEFT

    cart = d13.Cart(0, 0, 0, '<')
    assert cart.curr_turn == d13.LEFT
    cart.turn()
    assert cart.direction == 'v'
    assert cart.curr_turn == d13.STRAIGHT
    cart.turn()
    assert cart.direction == 'v'
    assert cart.curr_turn == d13.RIGHT
    cart.turn()
    assert cart.direction == '<'
    assert cart.curr_turn == d13.LEFT

    cart = d13.Cart(0, 0, 0, 'v')
    assert cart.curr_turn == d13.LEFT
    cart.turn()
    assert cart.direction == '>'
    assert cart.curr_turn == d13.STRAIGHT
    cart.turn()
    assert cart.direction == '>'
    assert cart.curr_turn == d13.RIGHT
    cart.turn()
    assert cart.direction == 'v'
    assert cart.curr_turn == d13.LEFT

    cart = d13.Cart(0, 0, 0, '^')
    assert cart.curr_turn == d13.LEFT
    cart.turn()
    assert cart.direction == '<'
    assert cart.curr_turn == d13.STRAIGHT
    cart.turn()
    assert cart.direction == '<'
    assert cart.curr_turn == d13.RIGHT
    cart.turn()
    assert cart.direction == '^'
    assert cart.curr_turn == d13.LEFT

def test_move():
    "Test moves."
    cart = d13.Cart(0, 0, 0, '>')
    cart.move()
    assert cart.x == 1
    assert cart.y == 0

    cart = d13.Cart(0, 0, 0, 'v')
    cart.move()
    assert cart.x == 0
    assert cart.y == 1

    cart = d13.Cart(0, 0, 0, '^')
    cart.move()
    assert cart.x == 0
    assert cart.y == -1

    cart = d13.Cart(0, 0, 0, '<')
    cart.move()
    assert cart.x == -1
    assert cart.y == 0

def test_update_direction():
    "Test update direction."
    cart = d13.Cart(0, 0, 0, '^')
    cart.update_direction('|')
    assert cart.direction == '^'
    cart.update_direction('/')
    assert cart.direction == '>'
    cart.update_direction('-')
    assert cart.direction == '>'
    cart.update_direction('\\')
    assert cart.direction == 'v'
    cart.update_direction('+')
    assert cart.direction == '>'

def read_test_ticks():
    "Read test ticks from file."
    with open('test_ticks.txt') as input_file:
        return input_file.read().split('\n%\n')[:-1]

def test_ticks():
    "Test ticks"
    with open('../test13.txt') as input_file:
        mine_map = d13.MineMap(input_file.readlines())
        test_ticks = read_test_ticks()
        assert test_ticks[0] == d13.map_to_string(mine_map.mine_map)
        for t in range(1, len(test_ticks)):
            mine_map.tick()
            assert test_ticks[t] == d13.map_to_string(mine_map.mine_map)

def test_solve_a():
    with open('../test13.txt') as input_file:
        mine_map = d13.MineMap(input_file.readlines())
        assert d13.solve_a(mine_map) == (7, 3)
    with open('../input13.txt') as input_file:
        mine_map = d13.MineMap(input_file.readlines())
        assert d13.solve_a(mine_map) == (58, 93)
