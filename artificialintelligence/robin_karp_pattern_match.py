# /tests/robin_karp_pattern_match.py
#
# Pattern match using the Robin-Karp method to optimize the inner loop
#
# See LICENCE.md for Copyright information
"""Loader module."""

import math

def match_pattern_robin_karp(pattern, text):
    """Matches patterns based on the Robin-Karp algorithm.

    First convert all of the text in the pattern to integers and then
    match the integers against each other. We use horners rule to
    progress along the text character-by-character.

    Matches are returned as a sequence of indices."""

    matches = []

    text_length = len(text)
    pattern_length = len(pattern)

    # First calcuate the integer representation of the pattern
    ascii_a_char_value = ord("a") - 1

    pattern_as_integer = 0
    for i in range(0, pattern_length):
        pattern_as_integer = (pattern_as_integer * 10 +
            ord(pattern[i]) - ascii_a_char_value)

    text_chunk_as_integer = 0
    for i in range(0, pattern_length):
        text_chunk_as_integer = (text_chunk_as_integer * 10 +
            ord(text[i]) - ascii_a_char_value)

    # Now progress along the text pattern, starting iterations at
    # 0 and comparing text_chunk_as_integer against
    # pattern_as_integer.
    for i in range(0, text_length - pattern_length + 1):

        if text_chunk_as_integer == pattern_as_integer:
            matches.append(i)

        # Now move the text chunk along, by doing the following:
        #
        # text_chunk_as_integer * 10 % (pow(10, pattern_length - 1)) +
        # text[i + pattern_length] - ascii_a_char_value
        if i < text_length - pattern_length:
            text_chunk_as_integer = ((text_chunk_as_integer %
                (math.pow(10, pattern_length - 1)) * 10) +
                ord(text[i + pattern_length]) - ascii_a_char_value)

    return matches