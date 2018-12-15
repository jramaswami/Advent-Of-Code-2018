import day15 as d15


def test_next_move():
    cave = d15.parse_cave(['#######', '#E..G.#', '#...#.#', '#.G.#G#', '#######'])
    assert d15.get_next_move(cave, d15.Posn(1, 1)) == d15.Posn(2, 1)
    cave = d15.parse_cave(['#######', '#.E...#', '#.....#', '#...G.#', '#######'])
    print(d15.cave_to_string(cave))
    assert d15.get_next_move(cave, d15.Posn(2, 1)) == d15.Posn(3, 1)
