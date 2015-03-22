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

# Generic rabin karp.
#
# You need to parse each character in your pattern and then convert it into
# an int. You multiple you hash by your alphabet size and then modulo prime.
#
# You always have to make sure that when there's a match on the hash that the
# text of the pattern itself also matches to avoid a false positive.
#
# Compute the hash of the pattern and the first m characters of the text and
# then just move along.
#
# cur = ((cur - (prev * high) % PRIME + PRIME) * ALPHABET + next) % PRIME
#
# The proof for this is that beacuse you've hashed your pattern and every time
# read the plaintext, you get to skip the inner-loop.
PRIME_NUMBER = 49157

def match_pattern_generic_rabin_karp(pattern, text):
    """Matches patterns based on the Robin-Karp algorithm.

    First convert all of the text in the pattern to integers and then
    match the integers against each other. We use horners rule to
    progress along the text character-by-character.

    Matches are returned as a sequence of indices."""

    matches = []

    def char_value(char):
        """Get the numeric value for this character."""
        return ord(char)

    alphabet_len = 256
    pattern_len = len(pattern)
    text_len = len(text)

    pattern_as_integer = 0
    text_chunk_as_integer = 0

    initial_value_hash = 1
    for i in range(0, pattern_len - 1):
        initial_value_hash = (initial_value_hash * alphabet_len) % PRIME_NUMBER

    # Construct initial hashes
    for i in range(0, pattern_len):
        pattern_as_integer = (alphabet_len * pattern_as_integer +
                              char_value(pattern[i])) % PRIME_NUMBER
        text_chunk_as_integer = (alphabet_len * text_chunk_as_integer +
                                 char_value(text[i])) % PRIME_NUMBER

    # Now progress along the text pattern, starting iterations at
    # 0 and comparing text_chunk_as_integer against
    # pattern_as_integer.
    for i in range(0, text_len - pattern_len + 1):

        # If there is a match, there may be a false positive, so
        # check the characters themselves for a match, then add a match
        if text_chunk_as_integer == pattern_as_integer:
            if text[i:i + pattern_len] == pattern:
                matches.append(i)

        # Now move the text chunk along, by doing the following:
        #
        # alphabet_len * (text_chunk_as_integer -                [ step 1 ] 
        #                 (initial_value_hash * char_value(text[i]))) +
        # char_value(text[i + pattern_len]) % PRIME_NUMBER       [ step 2 ]
        #
        # The first step takes our current hash value and subtracts its "head",
        # but moves it along by the length of the alphabet.
        #
        # The second step adds the current tail (eg, text[i + pattern_len])
        # modulo the prime number to the current hash.
        # 
        if i < text_len - pattern_len:
            text_chunk_as_integer = (alphabet_len * (text_chunk_as_integer -
                                                     initial_value_hash *
                                                     char_value(text[i])) +
                                     char_value(text[i + pattern_len])) % PRIME_NUMBER

            if text_chunk_as_integer < 0:
                text_chunk_as_integer += PRIME_NUMBER

    return matches
