# /tests/pattern_match_test.py
#
# Test cases for artificialintelligence.pattern_match_test
#
# See LICENCE.md for Copyright information
"""Test cases for usage of polysquarecmakelinter.main()."""

from artificialintelligence.naive_pattern_match import match_pattern_naive

from nose_parameterized import parameterized

from testtools import TestCase

pattern_matching_functions = [
    ("NaiveMatch", match_pattern_naive)
]

for pattern_matching_function in pattern_matching_functions:
    class TestPatternMatch(TestCase):

        """Test cases for pattern-matching functions.

        Pattern matching functions must have a signature like
        pattern(pat, text).
        """

        def __init__(self, *args, **kwargs):
            """Initialize members used by this class."""
            cls = TestPatternMatch
            super(cls, self).__init__(*args, **kwargs)  # pylint:disable=W0142
            self.matching_function = pattern_matching_function[1]

        @parameterized.expand([
            ("abc", "abbabcabba", [3]),
            ("daef", "dedfadaefdeafdaef", [5, 13])
        ])
        def test_find_alpha_patterns(self, pattern, haystack, expected_matches):
            """Test finding some simple alphabetical patterns."""

            self.assertEqual(expected_matches,
                             self.matching_function(pattern, haystack))

    TestPatternMatch.__name__ = "Test{0}".format(pattern_matching_function[0])
    exec("{0} = TestPatternMatch".format(TestPatternMatch.__name__))

