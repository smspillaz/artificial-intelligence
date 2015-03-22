# /tests/pattern_match_test.py
#
# Test cases for artificialintelligence.pattern_match_test
#
# See LICENCE.md for Copyright information
"""Test cases for usage of polysquarecmakelinter.main()."""

from artificialintelligence.naive_pattern_match import match_pattern_naive
from artificialintelligence.robin_karp_pattern_match import (match_pattern_robin_karp,
                                                             match_pattern_generic_rabin_karp)
from artificialintelligence.kmp_pattern_match import match_pattern_kmp
from artificialintelligence.boyer_moore_pattern_match import match_pattern_boyer_moore

from nose_parameterized import parameterized

from testtools import TestCase

pattern_matching_functions = {
    "NaiveMatch": match_pattern_naive,
    "RobinKarp": match_pattern_robin_karp,
    "GenericRabinKarp": match_pattern_generic_rabin_karp,
    "KMPMatch":  match_pattern_kmp,
    "BoyerMooreMatch": match_pattern_boyer_moore
}

tests = {}

def _create_pattern_match_test(name, match_function):
    class TestPatternMatch(TestCase):

        """Test cases for pattern-matching functions.

        Pattern matching functions must have a signature like
        pattern(pat, text).
        """

        def __init__(self, *args, **kwargs):
            """Initialize members used by this class."""
            cls = TestPatternMatch
            super(cls, self).__init__(*args, **kwargs)  # pylint:disable=W0142
            self.matching_function = match_function

        @parameterized.expand([
            ("abc", "abbabcabba", [3]),
            ("daef", "dedfadaefdeafdaef", [5, 13]),
            ("abcab", "abcabcabcab", [0, 3, 6])
        ])
        def test_find_alpha_patterns(self, pattern, haystack, expected_matches):
            """Test finding some simple alphabetical patterns."""

            self.assertEqual(expected_matches,
                             self.matching_function(pattern, haystack))

    name = "Test{0}".format(name)
    TestPatternMatch.__name__ = name
    return TestPatternMatch

for name, match_function in pattern_matching_functions.items():
    tests[name] = _create_pattern_match_test(name, match_function)

for name, test in tests.items():
    exec("{0} = test".format(name))
    del test

