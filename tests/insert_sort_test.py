# /tests/insert_sort_test.py
#
# Test cases for artificialintelligence.insert_sort
#
# See LICENCE.md for Copyright information
"""Test cases for usage of polysquarecmakelinter.main()."""

import random

from artificialintelligence.insert_sort import InsertSort

from nose_parameterized import parameterized, param

from testtools import TestCase

class TestInsertSort(TestCase):

    """Test cases for insert_sort."""

    data_to_insert_sort = [0]
    for i in range(0, 100):
        data_to_insert_sort.append(random.randint(1, 100))

    iterations = [param (i) for i in range(1, len(data_to_insert_sort))]

    @parameterized.expand(iterations)
    def test_n_one_items_always_sorted(self, iteration):
        """Test that n - 1 items are always sorted."""

        sort_object = InsertSort(TestInsertSort.data_to_insert_sort)

        for i in range(0, iteration):
            sort_object.iterate()

        self.assertEqual(sorted(sort_object.current_list()[0:iteration]),
                         sort_object.current_list()[0:iteration])

    def test_list_sorted_after_length_minus_one_iterations(self):
        """Test that list is sorted after len - 1 iterations."""

        sort_object = InsertSort(TestInsertSort.data_to_insert_sort)

        while sort_object.iterate():
            pass

        self.assertEqual(sorted(sort_object.current_list()),
                         sort_object.current_list())
