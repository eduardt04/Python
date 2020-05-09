from _operator import attrgetter
from copy import deepcopy
import numpy


class Node:
    def __init__(self, info):
        self.info = info


class Problem:
    def __init__(self, start=None, end=None):
        if start is None:
            start = [[2, 4, 3], [8, 7, 5], [1, 0, 6]]
        if end is None:
            end = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.start_node = Node(start)
        self.end_node = Node(end)
        self.N = len(start)


class IntermediaryNode:
    problem = None

    def __init__(self, node, parent=None, g=0, f=None):
        self.node = node
        self.parent = parent
        self.g = g

        if f is None:
            self.determine_f()
        else:
            self.f = f

    def determine_f(self):
        h = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if self.node.info[i][j] != 0:
                    h += abs(self.node.info[i][j] - (i * 3 + j + 1))
        self.f = h + self.g

    def get_intermediary_tree(self):
        temp_node = self
        tree = [temp_node]
        while temp_node.parent is not None:
            tree = [temp_node.parent] + tree
            temp_node = temp_node.parent
        return tree

    def already_in_tree(self, node):
        return node.node.info in [temp_node.node.info for temp_node in self.get_intermediary_tree()]

    def expand(self):
        next_moves = []
        free_position = (0, 0)

        for i in range(0, 3):
            for j in range(0, 3):
                if self.node.info[i][j] == 0:
                    free_position = (i, j)

        possible_moves = [numpy.subtract(free_position, (1, 0)), numpy.subtract(free_position, (0, 1)),
                          numpy.add(free_position, (1, 0)), numpy.add(free_position, (0, 1))]

        for move in possible_moves:
            if 0 <= move[0] < 3 and 0 <= move[1] < 3:
                child = IntermediaryNode(deepcopy(self.node), self, self.g + 1)
                child.node.info[free_position[0]][free_position[1]], child.node.info[move[0]][move[1]] = \
                    child.node.info[move[0]][move[1]], child.node.info[free_position[0]][free_position[1]]
                child.determine_f()
                next_moves.append(child)
        return next_moves

    def print_config(self):
        print(self.node.info)

    def test_end(self):
        return self.node.info == self.problem.end_node.info


def in_list(l, node):
    for i in range(len(l)):
        if l[i].node.info == node.node.info:
            return l[i]
    return None


def print_solution(end_node):
    tree = end_node.get_intermediary_tree()
    for node in tree:
        node.print_config()


def a_star():
    tree_root = IntermediaryNode(IntermediaryNode.problem.start_node)
    open = [tree_root]
    closed = []
    itrs = 0

    while len(open) > 0 and itrs < 15000:
        curr_node = open.pop(0)
        itrs += 1
        closed.append(curr_node)

        if curr_node.test_end():
            break

        for node in curr_node.expand():
            if not curr_node.already_in_tree(node):
                node_open = in_list(open, node)
                if node_open is not None and node_open.f > node.f:
                    open.remove(node_open)
                    open.append(node)
                node_closed = in_list(closed, node)
                if node_closed is not None and node_closed.f > node.f:
                    closed.remove(node_closed)
                    open.append(node)
                if node_closed is None and node_open is None:
                    open.append(node)
                open = sorted(sorted(open, key=attrgetter('g'), reverse=True), key=attrgetter('f'))

    print("\n------------------ Concluzie -----------------------")
    if len(open) == 0:
        print("Lista open e vida, nu avem drum solutie")
    else:
        print("Drum de cost minim: ")
        print_solution(curr_node)

if __name__ == "__main__":
    new_problem = Problem()
    IntermediaryNode.problem = new_problem
    a_star()
