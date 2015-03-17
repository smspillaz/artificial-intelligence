# /tests/tsp_mst.py
#
# Test cases for artificialintelligence.tsp_mst
#
# See LICENCE.md for Copyright information
"""Test cases for usage of artificialintelligence.tsp_mst."""

from artificialintelligence.tsp_mst import find_tsp_path
from artificialintelligence.tsp_mst import depth_first_search
from artificialintelligence.tsp_mst import MSTNode
from artificialintelligence.tsp_mst import TSPNode

from testtools import TestCase
from nose_parameterized import parameterized

from collections import namedtuple

MinimumSpanningTreeDFSSolution = namedtuple("MinimumSpanningTreeDFSSolution",
                                            ("mst_csr "
                                             "dfs_solution_zero "
                                             "dfs_solution_three"))

MINIMUM_SPANNING_TREES = [
    MinimumSpanningTreeDFSSolution(mst_csr=[[0, 0, 0, 3],
                                            [0, 0, 2, 0],
                                            [0, 0, 0, 5],
                                            [0, 0, 0, 0]],
                                   dfs_solution_zero=[
                                       MSTNode(0, 0),
                                       MSTNode(3, 3),
                                       MSTNode(2, 5),
                                       MSTNode(1, 2)
                                   ],
                                   dfs_solution_three=[
                                       MSTNode(3, 0),
                                       MSTNode(0, 3),
                                       MSTNode(2, 5),
                                       MSTNode(1, 2)
                                   ]),
    MinimumSpanningTreeDFSSolution(mst_csr=[[0, 0, 0, 3, 0],
                                            [0, 0, 2, 0, 0],
                                            [0, 0, 0, 5, 0],
                                            [0, 0, 0, 0, 8],
                                            [0, 0, 0, 0, 0]],
                                   dfs_solution_zero=[
                                       MSTNode(0, 0),
                                       MSTNode(3, 3),
                                       MSTNode(2, 5),
                                       MSTNode(1, 2),
                                       MSTNode(4, 8)
                                   ],
                                   dfs_solution_three=[
                                       MSTNode(3, 0),
                                       MSTNode(0, 3),
                                       MSTNode(2, 5),
                                       MSTNode(1, 2),
                                       MSTNode(4, 8)
                                   ])
]

class TestDepthFirstSearch(TestCase):

    """Tests for the depth_first_search function."""

    @parameterized.expand(MINIMUM_SPANNING_TREES)
    def test_search_minimum_spanning_tree(self,
                                          mst_csr,
                                          dfs_solution_zero,
                                          dfs_solution_three):
        """Search a minimum spanning tree in sparse format."""

        self.assertEqual(dfs_solution_zero,
                         depth_first_search(0, mst_csr))
        self.assertEqual(dfs_solution_three,
                         depth_first_search(3, mst_csr))

TravellingSalemanProblem = namedtuple("TravellingSalemanProblem",
                                      "tsp_cities tsp_path_bottom_right")

TRAVLLING_SALESMAN_PROBLEMS = [
    TravellingSalemanProblem(tsp_cities=[
                                 TSPNode(3, 0),
                                 TSPNode(0, 1),
                                 TSPNode(0, 0)
                             ],
                             tsp_path_bottom_right=[
                                 TSPNode(3, 0),
                                 TSPNode(0, 0),
                                 TSPNode(0, 1),
                                 TSPNode(3, 0)
                             ]),
    TravellingSalemanProblem(tsp_cities=[
                                 TSPNode(1, 3),
                                 TSPNode(0, 2),
                                 TSPNode(3, 2),
                                 TSPNode(1, 1),
                                 TSPNode(1, 0),
                                 TSPNode(3, 0)
                             ],
                             tsp_path_bottom_right=[
                                 TSPNode(3, 0),
                                 TSPNode(1, 0),
                                 TSPNode(1, 1),
                                 TSPNode(0, 2),
                                 TSPNode(1, 3),
                                 TSPNode(3, 2),
                                 TSPNode(3, 0)
                             ])
]

def find_bottomright_most_city(cities):
    """Finds the bottomright most city."""

    uppermost_x = 0
    lowermost_y = 99999999
    candidate = None

    for city_index in range(0, len(cities)):
        city = cities[city_index]
        if city.x >= uppermost_x and city.y <= lowermost_y:
            uppermost_x = city.x
            lowermost_y = city.y
            candidate = city_index

    assert candidate is not None
    return candidate

class TestTravellingSalesmanWithMST(TestCase):

    """Tests for solving the travelling salesman problem with und-graphs."""

    @parameterized.expand(TRAVLLING_SALESMAN_PROBLEMS)
    def test_travelling_salesman_problem(self, cities, expected_path):
        """Check that we have the expected path."""

        self.assertEqual(expected_path,
                         find_tsp_path(cities,
                                       find_bottomright_most_city(cities)))