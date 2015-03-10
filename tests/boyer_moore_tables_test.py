# /tests/pattern_match_test.py
#
# Test cases for artificialintelligence.pattern_match_test
#
# See LICENCE.md for Copyright information
"""Test cases for usage of polysquarecmakelinter.main()."""

from artificialintelligence.boyer_moore_pattern_match import (calculate_bad_character_table,
                                                              calculate_good_suffix_table)

from nose_parameterized import parameterized, param

from testtools import TestCase

EXPECTED_BAD_CHARACTER_TABLES = [
    param("abcab", {
        4: {
            "a": 1,
            "b": 3,
            "c": 2
        },
        3: {
            "a": 3,
            "b": 2,
            "c": 1
        },
        2: {
            "a": 2,
            "b": 1,
            "c": 0
        },
        1: {
            "a": 1,
            "b": 0,
            "c": 0 
        },
        0: {
            "a": 0,
            "b": 0,
            "c": 0
        }
    })
]

EXPECTED_GOOD_SUFFIX_TABLES = [
    param("nanbbbnan", {
        9: 0,
        8: 2,
        7: 6,
        6: 6,
        5: 0,
        4: 0,
        3: 0,
        2: 0,
        1: 0,
        0: 0
    })
]

class TestBoyerMooreTables(TestCase):
    """Test case for the Boyer-Moore tables."""

    @parameterized.expand(EXPECTED_BAD_CHARACTER_TABLES)
    def test_bad_character_tables(self, pattern, expected):
        """Calculate bad character table correctly."""

        self.assertEqual(expected,
                         calculate_bad_character_table(pattern,
                                                       set(pattern)))

    @parameterized.expand(EXPECTED_GOOD_SUFFIX_TABLES)
    def test_good_suffix_tables(self, pattern, expected):
        """Calculate good suffix table correctly."""

        self.assertEqual(expected,
                         calculate_good_suffix_table(pattern,
                                                     set(pattern)))
