"""
Advent of Code 2018
Day 7: The Sum of Its Parts
"""
from collections import defaultdict, namedtuple
from operator import attrgetter
import heapq

class Edge:
    "Edge class."
    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node
        self.open = True

    def __repr__(self):
        return self.from_node + "->" + self.to_node


class Graph:
    "Graph class."
    def __init__(self):
        self.edges_to = defaultdict(list)
        self.edges_from = defaultdict(list)
        self.nodes = defaultdict(bool)

    def __repr__(self):
        return 'edges to: ' + repr(self.edges_to) + "\n" + 'edges_from: ' + repr(self.edges_from)

    def add_edge(self, edge):
        self.edges_from[edge.from_node].append(edge)
        self.edges_to[edge.to_node].append(edge)
        self.nodes[edge.from_node] = False or self.nodes[edge.from_node]
        self.nodes[edge.to_node] = True

    def get_start(self):
        return [k for k, v in self.nodes.items() if not v]

    def has_edge_to(self, node):
        return any(e.open for e in self.edges_to[node])

    def get_edges_from(self, node):
        return self.edges_from[node]

    def get_edges_to(self, node):
        return self.edges_to[node]

    def dfs(self, node_v, path):
        "DFS"
        if not self.has_edge_to(node_v):
            path.append(node_v)
        for edge in sorted(self.get_edges_from(node_v), key=attrgetter('to_node')):
            if edge.open:
                # remove edge from node_v to node_w
                edge.open = False
                self.dfs(edge.to_node, path)

    def solveA(self):
        "Solve first part of puzzle."
        path = []
        for start in sorted(self.get_start()):
            self.dfs(start, path)
        return "".join(path)


def parse_input(input_string):
    "Parse input into a tuple of node->node."
    tokens = input_string.split()
    return Edge(tokens[1], tokens[7])


def solveB():
    "Solve second part of puzzle."
    pass


def main():
    "Main program."
    import sys
    graph = Graph()
    for ln in sys.stdin:
        edge = parse_input(ln)
        graph.add_edge(edge)
    print(graph.solveA())


if __name__ == '__main__':
    main()
