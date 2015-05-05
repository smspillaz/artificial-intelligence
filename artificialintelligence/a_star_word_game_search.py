# /tests/a_star_word_game_search.py
#
# Play the "word chess" game using the A* algorithm
#
# Here we'll need a heuristic to guess how far away we are from the goal. The
# simplest is simply just measuring how far away each letter is from its target
# (eg sum([abs(goal[i] - current[i]) for i, _ in enumerate(current)]))
#
# The A* algorithm at each node expanded and picks the one that's closest
# to the goal. The cost is just an ever-increasing "1", which increases each
# time we go down the tree.
#
# See LICENCE.md for Copyright information
"""Loader module."""

import os
from collections import namedtuple
from queue import PriorityQueue

import sympy

_ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def _get_valid_words(length):
    """Get a list of valid words."""

    path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(path,
                           "uninformed_word_game_search_word_list.txt")) as wd:
        return frozenset([w for w in wd.read().splitlines() if len(w) == length])


def _expand_word_at(word, index):
    """Expands the word into a set of subnodes."""

    combinations = []

    for c in _ALPHABET:
        if word[index] is not c:
            candidate = list(word)
            candidate[index] = c
            combinations.append(''.join(candidate))

    return combinations

VisitedNode = namedtuple("VisitedNode", "word depth")


class VisitedNodes(object):
    """Keeps a set of visited nodes."""

    def __init__(self):
        """Initialize this object."""

        super(VisitedNodes, self).__init__()
        self.visited_nodes = list()

    def visit_this_node(self, word):
        """Record that we've visited this word."""

        self.visited_nodes.append(word)

    def visited_already(self, word):
        """Returns true if we've already visited this node."""

        return word in self.visited_nodes

    def branching_factor_at_depth(self, depth):
        """Return branching factor for depth."""

        num_visited = len(self.visited_nodes)

        expression = "1"
        for i in range(0, depth):
            expression = expression + "+ b**{0} ".format(i + 1)

        b = sympy.symbols("b")

        to_eval = ("sympy.solve(sympy.Eq(" +
                   expression[2:] +
                   ", {0}".format(num_visited) + "), b)[-1].evalf()")
        return eval(to_eval)


DistanceNode = namedtuple("DistanceNode", "word distance")
Solution = namedtuple("Solution", "candidate depth")


def a_star_search(initial, goal):
    """Do an A* search to find the stages between our word and the goal."""

    class AStarNode(object):

        """A node for an a-star search."""

        def __lt__(self, other):
            """Returns true if cost + distance < other.cost + other.distance."""

            return ((self.accumulated_cost + self.distance) <
                    (other.accumulated_cost + other.distance))

        def __gt__(self, other):
            """Returns true if cost + distance > other.cost + other.distance."""

            return ((self.accumulated_cost + self.distance) >
                    (other.accumulated_cost + other.distance))

        def __init__(self, accumulated_cost, distance, parent, word):
            """Initialize this AStarNode."""

            super(AStarNode, self).__init__()
            self.accumulated_cost = accumulated_cost
            self.distance = distance
            self.word = word
            self.parent = parent

        def __str__(self):
            """String representation of this node."""

            return "[{0} -> {1}]".format(self.word, str(self.parent))

        def expand(self):
            """Return expansions of this node."""

            candidates = []
            for index in range(0, len(self.word)):
                candidates.extend(_expand_word_at(self.word, index))

            return [c for c in candidates if c in valid_words]

    assert len(initial) == len(goal)

    visited = VisitedNodes()
    expandable_nodes = PriorityQueue()
    valid_words = _get_valid_words(len(initial))

    def distance(w, g):
        """Estimate distance from word to goal."""

        return sum([(1 if g[i] != w[i] else 0) for i in range(0, len(w))])

    def traverse(current, goal):
        """The recursive-relation between current and goal."""

        candidates = [c for c in current.expand() if not visited.visited_already(c)]

        if len(candidates) == 0:
            return None

        for candidate in candidates:
            expandable_nodes.put(AStarNode(current.accumulated_cost + 1,
                                           distance(candidate, goal),
                                           current,
                                           candidate))

        while True:
            cand = expandable_nodes.get()
            visited.visit_this_node(cand.word)
            if cand.word != goal:
                traverse_result = traverse(cand, goal)
                if traverse_result is not None:
                    return traverse_result
            else:
                return Solution(candidate=cand, depth=cand.accumulated_cost)

    visited.visit_this_node(initial)
    solution = traverse(AStarNode(0,
                                  distance(initial, goal),
                                  None,
                                  initial),
                        goal)

    print("Branching factor for this solution " +
          str(visited.branching_factor_at_depth(solution.depth)))

    solution_list = []
    solution_node = solution.candidate
    while solution_node.parent is not None:
        solution_list.append(solution_node.word)
        solution_node = solution_node.parent

    return [initial] + list(reversed(solution_list))
