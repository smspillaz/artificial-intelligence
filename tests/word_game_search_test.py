# /tests/word_game_search_test.py
#
# Test cases for artificialintelligence.uninformed_word_game_search
#
# See LICENCE.md for Copyright information
"""Test cases for usage of polysquarecmakelinter.main()."""

from artificialintelligence.uninformed_word_game_search import (breadth_first_search,
                                                                limited_depth_first_search,
                                                                iterative_deepening_first_search)
from nose_parameterized import parameterized

from testtools import TestCase

pattern_search_functions = {
    "BFS": lambda _: breadth_first_search,
    "LimitedDepthFirstSearch": lambda l: lambda i, g: limited_depth_first_search(i, g, l),
    "IterativeDeepningFirstSearch": lambda l: lambda i, g: iterative_deepening_first_search(i ,g, l)
}

tests = {}

def _create_uninformed_search(name, search_function):
    class TestUninformedWordGameSearch(TestCase):

        """Test cases for pattern-matching functions.

        Pattern matching functions must have a signature like
        pattern(pat, text).
        """

        def __init__(self, *args, **kwargs):
            """Initialize members used by this class."""
            cls = TestUninformedWordGameSearch
            super(cls, self).__init__(*args, **kwargs)  # pylint:disable=W0142
            self.search_function = search_function

        @parameterized.expand([
            ("sick", "well", ["sick", "silk", "sill", "will", "well"])
        ])
        def test_find_word_chess(self, initial, goal, words):
            """Test finding words using word chess."""

            self.assertEqual(len(words),
                             len(self.search_function(len(words))(initial,
                                                                  goal)))

    name = "Test{0}".format(name)
    TestUninformedWordGameSearch.__name__ = name
    return TestUninformedWordGameSearch

for name, search_function in pattern_search_functions.items():
    tests[name] = _create_uninformed_search(name, search_function)

for name, test in tests.items():
    exec("{0} = test".format(name))
    del test

