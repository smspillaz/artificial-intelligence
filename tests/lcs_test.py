# /tests/lcs_test.py
#
# Test cases for artificialintelligence.lcs
#
# See LICENCE.md for Copyright information
"""Test cases for usage of artificialintelligence.lcs."""

from artificialintelligence.lcs import (lcs_length,
                                        longest_common_subsequence)

from nose_parameterized import parameterized

from testtools import TestCase

from collections import namedtuple

LongestCommonSubsequenceData = namedtuple("LongestCommonSubsequenceData",
                                          "seq_a seq_b expected_lcs")

LONGEST_COMMON_SUBSEQUENCE_TEST_DATA = [
    LongestCommonSubsequenceData(seq_a="BDCAB",
                                 seq_b="ABCB",
                                 expected_lcs="BCB"),
    LongestCommonSubsequenceData(seq_a="thisisatest",
                                 seq_b="testing123testing",
                                 expected_lcs="tsitest"),
    LongestCommonSubsequenceData(seq_a="1234",
                                 seq_b="1224533324",
                                 expected_lcs="1234")
]

class TestLongestCommonSubsequence(TestCase):

    """Test cases for longest_common_subsequence."""

    @parameterized.expand(LONGEST_COMMON_SUBSEQUENCE_TEST_DATA)
    def test_find_expected_lcs_length(self, seq_a, seq_b, expected_lcs):
        """Test that we find the expected length of our LCS."""

        actual_length, _ = lcs_length(seq_a, seq_b)

        self.assertEqual(len(expected_lcs), actual_length)

    @parameterized.expand(LONGEST_COMMON_SUBSEQUENCE_TEST_DATA)
    def test_find_expected_lcs(self, seq_a, seq_b, expected_lcs):
        """Test that we find the expected longest common subsequence."""

        self.assertEqual(expected_lcs, longest_common_subsequence(seq_a, seq_b))
