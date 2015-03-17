# /tests/mst_test.py
#
# Test cases for artificialintelligence.mst
#
# See LICENCE.md for Copyright information
"""Test cases for usage of artificialintelligence.mst."""

from artificialintelligence.mst import DisjointSet
from artificialintelligence.mst import minimum_spanning_tree

from testtools import TestCase
from nose_parameterized import parameterized

from collections import namedtuple

class TestDisjointSet(TestCase):

    """Test cases for the DisjointSet class."""

    def test_elements_all_in_disjoint_sets(self):
        """Test that all elements are initially in disjoint sets."""

        ds = DisjointSet([1, 2])

        self.assertNotEqual(ds.find(1), ds.find(2))

    def test_initial_elements_in_unique_same_set(self):
        """Test that all elements are part of their own set."""

        ds = DisjointSet([1, 2])
        self.assertEqual(ds.find(1), ds.find(1))

    def test_merging_a_set_makes_all_elements_in_same_set(self):
        """Test that merging a set causes all elements to be in same set."""

        ds = DisjointSet([1, 2])
        ds.merge(1, 2)
        self.assertEqual(ds.find(1), ds.find(2))


MinimumSpanningTreeSolution = namedtuple("MinimumSpanningTreeSolution",
                                         "undirected_graph mst")

MINIMUM_SPANNING_TREES = [
    MinimumSpanningTreeSolution(undirected_graph=[
                                    [0, 8, 0, 3],
                                    [8, 0, 2, 5],
                                    [0, 2, 0, 6],
                                    [3, 5, 6, 0]
                                ],
                                mst=[
                                    [0, 0, 0, 3],
                                    [0, 0, 2, 5],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0]
                                ]),
    MinimumSpanningTreeSolution(undirected_graph=[
                                    [0, 3, 0, 0, 1, 0, 0],
                                    [3, 0, 0, 0, 5, 0, 0],
                                    [0, 2, 0, 4, 0, 7, 0],
                                    [0, 0, 4, 0, 0, 2, 0],
                                    [1, 5, 0, 0, 0, 4, 6],
                                    [0, 0, 7, 2, 4, 0, 9],
                                    [0, 0, 0, 0, 6, 9, 0]
                                ],
                                mst=[
                                    [0, 3, 0, 0, 1, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0],
                                    [0, 2, 0, 4, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 2, 0],
                                    [0, 0, 0, 0, 0, 0, 6],
                                    [0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0]
                                ])
]


class TestMinimumSpanningTree(TestCase):

    """Test cases for finding minimum spanning trees."""

    @parameterized.expand(MINIMUM_SPANNING_TREES)
    def test_find_minimum_spanning_tree(self, undirected_graph, mst):
        """Test finding a minimum spanning tree."""

        self.assertEqual(mst, minimum_spanning_tree(undirected_graph))
