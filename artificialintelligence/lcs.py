# /tests/insert_sort.py
#
# Simple insert 
#
# See LICENCE.md for Copyright information
"""Loader module."""

from collections import namedtuple

class LCSTableDirection(object):

    def __init__(self):
        """Initializes this LCSTableDirection."""

        super(LCSTableDirection, self).__init__()

    Left = 1 # No common suffix found, highest value to left
    Up = 2 # No common suffix found, highest value above
    LeftOrUp = 3 # Highest value above or to left
    LeftAndUp = 4 # Suffix found, go diagonally to upper-left

LCSTableEntry = namedtuple("LCSTableEntry",
                           "sequence_length direction")

def lcs_length(seq_a, seq_b):
    """Returns table and length of longest common subsequence.

    This only returns the dynamic-programming table and the length of the
    longest common subsequence between sequence_a and sequence_b, but it
    doesn't return what that sequence is."""

    table_width = range(0, len(seq_a) + 1)
    table_height = range(0, len(seq_b) + 1)

    lcs_length_table = [[0 for i in table_width] for j in table_height]
    lcs_dir_table = [[None for i in table_width] for j in table_height]

    for i in range(0, len(seq_b)):
        for j in range(0, len(seq_a)):
            if seq_b[i] != seq_a[j]:
                # Remember, there's an offset of -1 by default
                if lcs_length_table[i][j + 1] > lcs_length_table[i + 1][j]:
                    lcs_length_table[i + 1][j + 1] = lcs_length_table[i][j + 1]
                    lcs_dir_table[i + 1][j + 1] = LCSTableDirection.Up
                elif lcs_length_table[i][j + 1] < lcs_length_table[i + 1][j]:
                    lcs_length_table[i + 1][j + 1] = lcs_length_table[i + 1][j]
                    lcs_dir_table[i + 1][j + 1] = LCSTableDirection.Left
                elif lcs_length_table[i][j + 1] == lcs_length_table[i + 1][j]:
                    lcs_length_table[i + 1][j + 1] = lcs_length_table[i + 1][j]
                    lcs_dir_table[i + 1][j + 1] = LCSTableDirection.LeftOrUp
            else:
                # We found a match, so take the sequence pointer from the upper
                # left corner and increment it here
                lcs_length_table[i + 1][j + 1] = lcs_length_table[i][j] + 1
                lcs_dir_table[i + 1][j + 1] = LCSTableDirection.LeftAndUp

    return lcs_length_table[len(seq_b)][len(seq_a)], lcs_dir_table


def longest_common_subsequence(seq_a, seq_b):
    """Return the longest common subsequence for seq_a and seq_b."""

    sequence_length, direction_table = lcs_length(seq_a, seq_b)

    # Start at the end of the direction table (eg, len(seq_a), len(seq_b)
    # and go backwards in the direction of the arrows. If we take an
    # upper-left arrow, then made a note of the x - 1, y - 1 cell that we're
    # in as an index into both sequences. Both letters should line up. Prepend
    # the letter to subsequence)

    current_subsequence = ""

    seq_a_table_index = len(seq_a)
    seq_b_table_index = len(seq_b)

    while sequence_length > 0:
        assert not (seq_a_table_index == 0 and seq_b_table_index == 0)

        if (direction_table[seq_b_table_index][seq_a_table_index] ==
                LCSTableDirection.Left):
            seq_a_table_index -= 1
            assert seq_a_table_index > -1
        elif (direction_table[seq_b_table_index][seq_a_table_index] ==
                LCSTableDirection.Up):
            seq_b_table_index -= 1
            assert seq_b_table_index > -1
        elif (direction_table[seq_b_table_index][seq_a_table_index] ==
                LCSTableDirection.LeftOrUp):
            seq_a_table_index -= 1 # Just go to the left in this case
            assert seq_a_table_index > -1
        elif (direction_table[seq_b_table_index][seq_a_table_index] ==
                LCSTableDirection.LeftAndUp):
            # We made a left-and-up jump, so assert that we're on the same
            # character, note it down and decrement the remaining sequence
            # length
            assert seq_a[seq_a_table_index - 1] == seq_b[seq_b_table_index - 1]
            current_subsequence = (seq_a[seq_a_table_index - 1] +
                                   current_subsequence)
            seq_a_table_index -= 1
            seq_b_table_index -= 1
            sequence_length -= 1
            assert seq_a_table_index > -1
            assert seq_b_table_index > -1
        else:
            raise RuntimeError("Code not reachable - {0} remains".format(sequence_length))

    return current_subsequence
