# /tests/knapsack_test.py
#
# Test cases for artificialintelligence.knapsack
#
# See LICENCE.md for Copyright information
"""Test cases for usage of polysquarecmakelinter.main()."""

from artificialintelligence.knapsack import (knapsack,
                                             items_for_knapsack)

from nose_parameterized import parameterized, param

from testtools import TestCase

from collections import namedtuple

Item = namedtuple("Item", "value cost")

class TestKnapsack(TestCase):

    """Test cases for knapsack."""

    items = [
        Item(value=1, cost=2),
        Item(value=2, cost=3),
        Item(value=7, cost=9),
        Item(value=4, cost=4),
    ]

    expected_value_of_knapsack = {
        0: [],
        1: [],
        2: [1],
        3: [2],
        4: [4],
        5: [4],
        6: [4, 1],
        7: [4, 2],
        8: [4, 2],
        9: [7],
        10: [7],
        11: [6, 1]
    }

    @parameterized.expand([param (i) for i in range(0, 11)])
    def test_knapsack_has_expected_items_for_capacity(self, capacity):
        """Test that the knapsack has the correct items for its capacity."""

        self.assertEqual(sum(TestKnapsack.expected_value_of_knapsack[capacity]),
                         knapsack(TestKnapsack.items, capacity)[1])


    unequal_items = [
        Item(value=5, cost=5),
        Item(value=5, cost=5),
        Item(value=6, cost=9)
    ]

    def test_knapsack_doesnt_use_greedy(self):
        """Test that the knapsack picks the two value five items."""

        self.assertEqual(10, knapsack(TestKnapsack.unequal_items, 10)[1])

    @parameterized.expand([param (i) for i in range(0, 11)])
    def test_can_pick_right_items_for_knapsack_capacity(self, capacity):
        """Test that we can pick the right items for the knapsack's capacity."""

        self.assertEqual(TestKnapsack.expected_value_of_knapsack[capacity],
                         list(reversed(sorted(items_for_knapsack(TestKnapsack.items,
                                                                 capacity)))))
