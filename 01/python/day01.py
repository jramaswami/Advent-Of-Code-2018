"""
Advent of Code :: 2018
Day 1: Chronal Calibration
"""

def solveB(data):
    "Solve second part of problem."
    from itertools import accumulate, cycle
    freqs = dict()
    freqs[0] = 1
    for freq in accumulate(cycle(data)):
        if freq in freqs:
            return freq
        freqs[freq] = 1


def solveA(data):
    "Solve first part of problem."
    return sum(data)


def main():
    "Main program."
    import sys
    data = [int(i) for i in sys.stdin.readlines()]
    print(solveA(data))
    print(solveB(data))


if __name__ == '__main__':
    main()
