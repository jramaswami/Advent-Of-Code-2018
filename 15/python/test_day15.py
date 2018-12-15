"""
Advent of Code 2018
Day 15: Beverage Bandits
Tests
"""
import day15 as d15

def test_find_nearest_enemy_space():
    grid = d15.grid_from_file('../test_grid2.txt')
    assert grid.units[0].find_nearest_enemy_space() == d15.Posn(3, 1)

def test_find_next_step():
    grid = d15.Grid(['#######', '#.E...#', '#.....#', '#...G.#', '#######'])
    assert grid.units[0].find_nearest_enemy_space() == d15.Posn(4, 2)
    assert grid.units[0].find_next_step() == d15.Posn(3, 1)

def test_tick():
    init = ['#########', '#G..G..G#', '#.......#', '#.......#', '#G..E..G#',
            '#.......#', '#.......#', '#G..G..G#', '#########']
    expected = [['#########', '#.G...G.#', '#...G...#', '#...E..G#', '#.G.....#',
                 '#.......#', '#G..G..G#', '#.......#', '#########'],
                ['#########', '#..G.G..#', '#...G...#', '#.G.E.G.#', '#.......#',
                 '#G..G..G#', '#.......#', '#.......#', '#########'],
                ['#########', '#.......#', '#..GGG..#', '#..GEG..#', '#G..G...#',
                 '#......G#', '#.......#', '#.......#', '#########']]
    grid = d15.Grid(init)
    for t in range(3):
        grid.tick()
        assert str(grid) == "\n".join(expected[t])

def test_combat():
    init = ['#######', '#.G...#', '#...EG#', '#.#.#G#', '#..G#E#', '#.....#', '#######']
    grid = d15.Grid(init)

    # after round 1
    grid.tick()
    assert str(grid) == '#######\n#..G..#\n#...EG#\n#.#G#G#\n#...#E#\n#.....#\n#######'
    assert len(grid.units) == 6
    assert grid[d15.Posn(3, 1)].utype == 'G'
    assert grid[d15.Posn(3, 1)].hitpoints == 200
    assert grid[d15.Posn(4, 2)].utype == 'E'
    assert grid[d15.Posn(4, 2)].hitpoints == 197

    # after round 2
    grid.tick()
    assert str(grid) == '#######\n#...G.#\n#..GEG#\n#.#.#G#\n#...#E#\n#.....#\n#######'

    # after round 23
    while grid.time < 23:
        grid.tick()
    assert str(grid) == '#######\n#...G.#\n#..G.G#\n#.#.#G#\n#...#E#\n#.....#\n#######'
    assert len(grid.units) == 5

    # after round 24
    grid.tick()
    print(grid)
    assert str(grid) == '#######\n#.G...#\n#..G..#\n#.#.#G#\n#..G#E#\n#.....#\n#######'

