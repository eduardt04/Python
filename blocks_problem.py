from _operator import attrgetter
from copy import deepcopy


class Node:
    def __init__(self, info):
        self.info = info


class Problem:
    def __init__(self, start=None, end=None):
        if start is None:
            start = [['a', 'h'], ['c', 'b', 'g'], ['d', 'e', 'f']]
        if end is None:
            end = [['b', 'c'], ['e', 'h', 'f'], ['d', 'a', 'g']]

        self.start_node = Node(start)
        self.end_node = Node(end)

        self.stacks_nr = len(start)
        self.cubes_nr = sum([len(stack) for stack in start])

    def search_letter_end_position(self, letter):
        for i in range(0, self.stacks_nr):
            for j in range(0, self.end_node.info[i].__len__()):
                if self.end_node.info[i][j] == letter:
                    return i, j


class IntermediaryNode:
    problem = None

    def __init__(self, node, parent=None, g=0, f=None):
        self.node = node
        self.parent = parent
        self.g = g

        if f is None:
            self.f = self.g + self.determine_h()
        else:
            self.f = f + self.determine_h()

    def search_letter_position(self, letter):
        for i in range(0, self.problem.stacks_nr):
            for j in range(0, self.node.info[i].__len__()):
                if self.node.info[i][j] == letter:
                    return i, j

    def determine_h(self):
        h = 0
        for i in range(self.problem.cubes_nr):
            current_letter = chr(ord('a') + i)
            config_stack, config_stack_position = self.search_letter_position(current_letter)
            end_stack, end_stack_position = self.problem.search_letter_end_position(current_letter)
            if config_stack != end_stack or config_stack_position != end_stack_position:
                h = h + max(0, self.node.info[config_stack].__len__() - config_stack_position - 1) + \
                    abs(self.problem.end_node.info[end_stack].__len__() - end_stack_position)
        return h

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
        for i in range(0, self.problem.stacks_nr):
            for j in range(0, self.problem.stacks_nr):
                if self.node.info[i].__len__() > 0 and i != j:
                    child = IntermediaryNode(deepcopy(self.node), self, self.g+1)
                    child.node.info[j].append(child.node.info[i].pop(-1))
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

    while len(open) > 0:
        curr_node = open.pop(0)
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
