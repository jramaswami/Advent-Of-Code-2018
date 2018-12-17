"""
Advent of Code 2018
Day 2 ::
"""
from collections import Counter

def off_by_one(data):
    "Find the two ids that differ by one character."
    for index, box_id0 in enumerate(data):
        for box_id1 in data[index+1:]:
            delta = 0
            for ltr0, ltr1 in zip(box_id0, box_id1):
                if ltr0 != ltr1:
                    delta += 1
                    if delta > 1:
                        break
            if delta == 1:
                return box_id0, box_id1


def common_letters(box_id0, box_id1):
    "Return common letters as a string."
    common = []
    for ltr0, ltr1 in zip(box_id0, box_id1):
        if ltr0 == ltr1:
            common.append(ltr0)
    return "".join(common)


def solveB(data):
    "Solve second part of the puzzle."
    box_id0, box_id1 = off_by_one(data)
    return common_letters(box_id0, box_id1)


def solveA(data):
    "Solve first part of puzzle."
    threes = 0
    twos = 0
    for box_id in data:
        is_two = 0
        is_three = 0
        cntr = Counter(box_id)
        for ltr, freq in cntr.items():
            if freq == 3:
                is_three = 1
            elif freq == 2:
                is_two = 1
        twos += is_two
        threes += is_three
    return twos * threes


def main():
    "Main program."
    import sys
    data = [s.strip() for s in sys.stdin.readlines()]
    print(solveA(data))
    print(solveB(data))


if __name__ == '__main__':
    main()

