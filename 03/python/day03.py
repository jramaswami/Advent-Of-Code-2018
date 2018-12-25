"""
Advent of Code 2018
Day 3: No Matter How You Slice It
"""
from collections import namedtuple

Claim = namedtuple('Claim', ['id', 'x', 'y', 'width', 'height'])
Fabric = namedtuple('Fabric', ['map', 'claim_count'])


def parse_claim(input_string):
    "Parse the input string into claim."
    tokens = input_string.split()
    claim_id = int(tokens[0][1:])
    x, y = (int(i) for i in tokens[2][:-1].split(','))
    ht, wd = (int(i) for i in tokens[3].split('x'))
    return Claim(claim_id, x, y, ht, wd)


def map_claims(claims, size=1000):
    "Create a map of the claims."
    fabric_map = [[set() for _ in range(size)] for _ in range(size)]
    for claim in claims:
        for y in range(claim.y, claim.y + claim.height):
            for x in range(claim.x, claim.x + claim.width):
                fabric_map[y][x].add(claim.id)
    return Fabric(fabric_map, len(claims))


def solveA(fabric):
    "Solve first part of puzzle."
    return sum(sum(1 if len(x) > 1 else 0 for x in row) for row in fabric.map)


def solveB(fabric):
    "Solve second part of puzzle."
    conflicts = {}
    for row in fabric.map:
        for claims in row:
            for claim in claims:
                if len(claims) > 1:
                        conflicts[claim] = True
    for claim_id in range(1, fabric.claim_count + 1):
        if claim_id not in conflicts:
            return claim_id


def main():
    "Main program."
    import sys
    claims = [parse_claim(line.strip()) for line in sys.stdin.readlines()]
    fabric = map_claims(claims, 1000)
    print(solveA(fabric))
    print(solveB(fabric))


if __name__ == '__main__':
    main()
