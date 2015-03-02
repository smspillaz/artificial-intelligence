# /tests/naive_pattern_match.py
#
# Naive pattern matching
#
# See LICENCE.md for Copyright information
"""Loader module."""

def match_pattern_naive(pattern, text):
    """Matches patterns based on a naive algorithm.

    Patterns are matched on the basis of iterating through an outer loop
    to for each character of text - len(pattern) and then each subsequence
    text[n:len(pattern)] is checked against pattern.

    Matches are returned as a sequence of indices."""

    text_length = len(text)
    pattern_length = len(pattern) 

    matches = []

    for i in range(0, text_length - pattern_length + 1):
        match = True
        for j in range(0, pattern_length):
            if pattern[j] != text[i + j]:
                match = False

        if match:
            matches.append(i)

    return matches