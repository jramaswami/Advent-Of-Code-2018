import day15 as d15


def test_next_move():
    cave, _ = d15.parse_cave(['#######', '#E..G.#', '#...#.#', '#.G.#G#', '#######'])
    assert d15.get_next_move(cave, d15.Posn(1, 1)) == d15.Posn(2, 1)
    cave, _ = d15.parse_cave(['#######', '#.E...#', '#.....#', '#...G.#', '#######'])
    print(d15.cave_to_string(cave))
    assert d15.get_next_move(cave, d15.Posn(2, 1)) == d15.Posn(3, 1)

def test_no_combat_ticks():
    cave, hp = d15.cave_from_file('../no_combat0.txt')
    d15.tick(cave, hp)
    expected_cave, hp = d15.cave_from_file('../no_combat1.txt')
    assert d15.cave_to_string(cave, no_ids=True) == d15.cave_to_string(expected_cave, no_ids=True)
    d15.tick(cave, hp)
    expected_cave, hp = d15.cave_from_file('../no_combat2.txt')
    assert d15.cave_to_string(cave, no_ids=True) == d15.cave_to_string(expected_cave, no_ids=True)
    d15.tick(cave, hp)
    expected_cave, hp = d15.cave_from_file('../no_combat3.txt')
    assert d15.cave_to_string(cave, no_ids=True) == d15.cave_to_string(expected_cave, no_ids=True)

def read_combat_file(filename):
    with open(filename) as inputf:
        return inputf.read().strip()


def show_tick_files(actual, expected):
    print('expected')
    print(expected)
    print('---')
    print('actual')
    print(actual)
    print('---')

def test_combat():
    cave, hp = d15.cave_from_file('../combat_init.txt')
    expected = read_combat_file('../combat0.txt')
    actual = d15.tick_to_string(cave, hp)
    assert actual == expected
    print("TICK 1")
    d15.tick(cave, hp)
    expected = read_combat_file('../combat1.txt')
    actual = d15.tick_to_string(cave, hp)
    assert actual == expected
    print("TICK 2")
    d15.tick(cave, hp)
    expected = read_combat_file('../combat2.txt')
    actual = d15.tick_to_string(cave, hp)
    assert actual == expected
    for t in range(3, 24):
        print("TICK", t)
        d15.tick(cave, hp)
    expected = read_combat_file('../combat23.txt')
    actual = d15.tick_to_string(cave, hp)
    assert actual == expected
    print("TICK 24")
    d15.tick(cave, hp)
    expected = read_combat_file('../combat24.txt')
    actual = d15.tick_to_string(cave, hp)
    assert actual == expected
    print("TICK 25")
    d15.tick(cave, hp)
    expected = read_combat_file('../combat25.txt')
    actual = d15.tick_to_string(cave, hp)
    assert actual == expected
    print("TICK 26")
    d15.tick(cave, hp)
    expected = read_combat_file('../combat26.txt')
    actual = d15.tick_to_string(cave, hp)
    assert actual == expected
    print("TICK 27")
    d15.tick(cave, hp)
    expected = read_combat_file('../combat27.txt')
    actual = d15.tick_to_string(cave, hp)
    assert actual == expected
    print("TICK 28")
    d15.tick(cave, hp)
    expected = read_combat_file('../combat28.txt')
    actual = d15.tick_to_string(cave, hp)
    assert actual == expected
    # show_tick_files(actual, expected)
    # print(d15.cave_to_string(cave))

def test_solve_a():
    cave, hp = d15.cave_from_file('../combat_init.txt')
    assert d15.solve_a(cave, hp) == 27730
    expected = read_combat_file('../combat47.txt')
    actual = d15.tick_to_string(cave, hp)
    assert actual == expected

    cave, hp = d15.cave_from_file('../combatB_init.txt')
    assert d15.solve_a(cave, hp) == 36334
    expected = read_combat_file('../combatB_final.txt')
    actual = d15.tick_to_string(cave, hp)
    assert actual == expected

    cave, hp = d15.cave_from_file('../combatC_init.txt')
    assert d15.solve_a(cave, hp) == 39514
    expected = read_combat_file('../combatC_final.txt')
    actual = d15.tick_to_string(cave, hp)

    cave, hp = d15.cave_from_file('../combatD_init.txt')
    assert d15.solve_a(cave, hp) == 27755
    expected = read_combat_file('../combatD_final.txt')
    actual = d15.tick_to_string(cave, hp)
    assert actual == expected

    cave, hp = d15.cave_from_file('../combatE_init.txt')
    assert d15.solve_a(cave, hp) == 28944
    expected = read_combat_file('../combatE_final.txt')
    actual = d15.tick_to_string(cave, hp)
    assert actual == expected

    cave, hp = d15.cave_from_file('../combatF_init.txt')
    assert d15.solve_a(cave, hp) == 18740
    expected = read_combat_file('../combatF_final.txt')
    actual = d15.tick_to_string(cave, hp)
    assert actual == expected

def test_solve_b():
    cave, hp = d15.cave_from_file('../elf_power_combatA.txt')
    assert d15.solve_b(cave, hp) == 4988
    # expected = read_combat_file('../combatF_final.txt')
    # actual = d15.tick_to_string(cave, hp)
    # assert actual == expected
    cave, hp = d15.cave_from_file('../elf_power_combatB.txt')
    assert d15.solve_b(cave, hp) == 31284
    cave, hp = d15.cave_from_file('../elf_power_combatC.txt')
    assert d15.solve_b(cave, hp) == 3478
    cave, hp = d15.cave_from_file('../elf_power_combatD.txt')
    assert d15.solve_b(cave, hp) == 6474
    cave, hp = d15.cave_from_file('../elf_power_combatE.txt')
    assert d15.solve_b(cave, hp) == 1140


    # print(d15.cave_to_string(cave))

