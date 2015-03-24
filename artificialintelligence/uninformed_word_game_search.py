# /tests/uninformed_word_game_search.py
#
# Play the "word chess" game using uninformed search algorithms to find valid
# solutions.
#
# Effectively, for a word W, there will be pow(26, 4) (i.e 45976) different
# combinations of letters that may get us to another valid word. Only one
# letter at a time can be changed.
#
# There are different kinds of algorithms that we can use to run the
# search space.
#
# See LICENCE.md for Copyright information
"""Loader module."""

import os
from collections import namedtuple

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


def _candidate_combinations(word, index, valid, visited, depth):
    """Gets a list of candidate combinations."""

    return [w for w in _expand_word_at(word, index) if w in valid and not visited.visited_already(w, depth)]


VisitedNode = namedtuple("VisitedNode", "word depth")

class VisitedNodes(object):
    """Keeps a set of visited nodes at each depth."""

    def __init__(self):
        """Initialize this object."""

        super(VisitedNodes, self).__init__()
        self.visited_nodes = list()

    def visit_this_node(self, word, depth):
        """Record that we've visited this word at this depth."""

        self.visited_nodes.append(VisitedNode(word, depth))

    def visited_already(self, word, depth):
        """Returns true if we've already visited this node."""

        for node in self.visited_nodes:
            if node.word == word and node.depth <= depth:
                return True

        return False


def breadth_first_search(initial, goal):
    """Do a breadth-first-search to find the stages between our goal word."""

    Node = namedtuple("Node", "word parent depth")

    assert len(initial) == len(goal)

    valid_words = _get_valid_words(len(goal))
    visited_nodes = VisitedNodes()
    nodes_to_expand =[Node(word=initial, parent=None, depth = 0)]

    while len(nodes_to_expand) > 0:
        # Expand all the nodes to get a list of nodes to search. Reset
        # nodes_to_expand and then expand them all again

        candidate_nodes = []

        for node in nodes_to_expand:
            if node.word == goal:
                path = []
                while node is not None:
                    path.append(node.word)
                    node = node.parent

                return list(reversed(path))
            else:
                for i in range(0, len(node.word)):
                    candidate_nodes += [Node(word=w, parent=node, depth=node.depth + 1) for w in
                                        _candidate_combinations(node.word, 
                                                                i,
                                                                valid_words,
                                                                visited_nodes,
                                                                node.depth + 1)]

        nodes_to_expand = candidate_nodes
        for n in candidate_nodes:
            visited_nodes.visit_this_node(n.word, n.depth)


def depth_first_search(initial, goal):
    """Perform a depth first search.

    The reason why this looks so odd is that we very quickly run into
    problems with python's recursion limit, so every variable needs to be
    a stack."""

    assert len(initial) == len(goal)

    valid_words = _get_valid_words(len(initial))
    visited_nodes = VisitedNodes()

    word_path_stack = { 0: [], 1: [initial] }
    word_stack = { 0: "", 1: initial }
    word_index_stack = { 0: 0, 1: 0 }
    combination_stack = { 0: [] }
    combination_index_stack = { 0: 0, 1: 0 }

    tree_level = 1
    current_word = word_stack[tree_level]

    def _get_combinations(tree_level, word, index, valid_words, visited_nodes):
        """Try and get a pre-computed list of combinations to resume from.

        If its not available just recalculate it."""

        try:
            return combination_stack[tree_level]
        except KeyError:
            combination_stack[tree_level] = _candidate_combinations(current_word,
                                                                    i,
                                                                    valid_words,
                                                                    visited_nodes)
            return combination_stack[tree_level]

    solutions = []

    while tree_level > 0:
        current_word = word_stack[tree_level]

        bailout = False

        for i in range(word_index_stack[tree_level], len(current_word)):
            combinations = _get_combinations(tree_level,
                                             current_word,
                                             i,
                                             valid_words,
                                             visited_nodes,
                                             tree_level + 1)

            for j in range(combination_index_stack[tree_level],
                           len(combinations)):
                combination = combinations[j]
                if combination == goal:
                    solutions.append(word_path_stack[tree_level - 1] + [goal])
                else:
                    # Save state, resume from next combination index, but
                    # this word index
                    word_index_stack[tree_level] = i
                    combination_index_stack[tree_level]= j + 1

                    # Reset everything from this point onwards
                    tree_level += 1
                    visited_nodes.visit_this_node(combination, tree_level)
                    word_stack[tree_level] = combination
                    word_path_stack[tree_level] = (word_path_stack[tree_level - 1] +
                                                   [combination])
                    combination_index_stack[tree_level] = 0
                    word_index_stack[tree_level] = 0

                    bailout = True
                    break

            if bailout:
                break

            # Reset combination index stack, as we've completed the loop
            combination_index_stack[tree_level] = 0
            del combination_stack[tree_level]

        # Bailing out - contine this while loop with our incremented tree level
        if bailout:
            continue

        tree_level -= 1
        word_index_stack[tree_level] = 0

    return list(sorted(solutions, key=lambda x: len(x)))[0]

def limited_depth_first_search(initial, goal, limit):
    """Perform a depth first search to get from initial to goal.

    The limit on the path size is limit. Any more than that and we don't
    recurse."""

    assert len(initial) == len(goal)

    valid_words = _get_valid_words(len(initial))
    visited_nodes = VisitedNodes()

    solutions = []

    def recurse(current_word, path, goal, depth):
        """Recurse into our depth-first search tree."""

        if current_word == goal:
            solutions.append(path)
        else:
            for i in range(0, len(current_word)):
                candidate_combinations = _candidate_combinations(current_word,
                                                                 i,
                                                                 valid_words,
                                                                 visited_nodes,
                                                                 depth + 1)

                for combination in candidate_combinations:
                    visited_nodes.visit_this_node(combination, depth)
                    if depth < limit:
                        recurse(combination,
                                path + [combination],
                                goal,
                                depth + 1)

    recurse(initial, [initial], goal, 0)

    if len(solutions) > 0:
        return list(sorted(solutions, key=lambda x: len(x)))[0]
    else:
        return None


def iterative_deepening_first_search(initial, goal, limit):
    """Perform an interative deepening depth first search."""

    for i in range(0, limit + 1):
        candidate_solution = limited_depth_first_search(initial, goal, i)
        if candidate_solution is not None:
            return candidate_solution

    return None
