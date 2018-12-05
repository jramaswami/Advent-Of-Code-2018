"""
Advent of Code 2018
Day 5: Alchemical Reduction
"""


def are_opposites(lhs, rhs):
    "Returns true if the two characters are polar opposites."
    if lhs.islower() and rhs.isupper() and lhs == rhs.lower():
        return True
    if lhs.isupper() and rhs.islower() and lhs == rhs.upper():
        return True
    return False


def solveA(polymer):
    "Solve first part of puzzle."
    print(polymer)
    total_units = len(polymer)
    curr_index = 1
    prev_index = 0
    while curr_index < len(polymer):
        print('\tcomparing', polymer[prev_index], prev_index, polymer[curr_index], curr_index)
        if are_opposites(polymer[prev_index], polymer[curr_index]):
            print('\tdestroying', polymer[prev_index], polymer[curr_index])
            total_units -= 2
            prev_index -= 1
            if prev_index < 0:
                prev_index = curr_index
            curr_index += 1
        else:
            prev_index += 1
            curr_index += 1

    return total_units


def main():
    "Main program."
    import sys
    data = sys.readline().strip()


if __name__ == '__main__':
    main()
