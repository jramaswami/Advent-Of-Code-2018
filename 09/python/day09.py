"""
Advent of Code 2018
Day 9: Marble Mania
"""

class Marble:
    "Marble in circle"
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

class MarbleCircleIterator:
    "Iterator for marble circle"
    def __init__(self, head, special):
        self.curr = head
        self.special = special

    def __iter__(self):
        return self

    def __next__(self):
        "Iterator"
        if self.curr is None:
            raise StopIteration
        else:
            value = self.curr.value
            self.curr = self.curr.next
            if value == self.special:
                return -value
            return value


class MarbleCircle:
    "Marble circle"
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def special_insert(self, value):
        "Remove marbles instead of inserting."
        score = value
        node_to_remove = self.current
        for _ in range(7):
            if node_to_remove.prev is None:
                node_to_remove = self.tail
            else:
                node_to_remove = node_to_remove.prev
        return node_to_remove.value

    def insert(self, value):
        "Insert new value in marble circle"
        if value and value % 23 == 0:
            return self.special_insert(value)

        new_current_node = Marble(value)
        if self.head is None:
            self.current = self.head = self.tail = new_current_node
            return

        if self.current.next == None:
            new_prev_node = self.head
        else:
            new_prev_node = self.current.next

        new_next_node = new_prev_node.next

        if new_prev_node:
            new_prev_node.next = new_current_node
        new_current_node.prev = new_prev_node

        new_current_node.next = new_next_node
        if new_next_node:
            new_next_node.prev = new_current_node
        else:
            self.tail = new_current_node
        new_current_node.next = new_next_node
        return 0

    def __iter__(self):
        return MarbleCircleIterator(self.head, self.current.value)

    def __repr__(self):
        return repr([i for i in self])


def parse_input(input_string):
    "Parse input string, returning number of players and last marble value."
    tokens = input_string.split()
    return (int(tokens[0]), int(tokens[6]))


def solveA(players, last_marble):
    "Solve first part of puzzle."
    pass


def solveB():
    "Solve second part of puzzle."
    pass


def main():
    "Main program."
    import sys
    players, last_marble = parse_input(sys.stdin.readline())
    print(players, last_marble)



if __name__ == '__main__':
    main()