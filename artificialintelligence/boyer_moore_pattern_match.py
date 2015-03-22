# /tests/boyer_moore_pattern_match.py
#
# Pattern match using the Boyer-Moore method to optimize the outer loop
#
# See LICENCE.md for Copyright information
"""Knuth pattern matching method."""

import sys

def calculate_bad_character_table(pattern,
                                  available_characters):
    """Calculate bad character lookup table.

    The table should have each index in the pattern and for each
    character, indicate how much we need to jump back in order to
    reach the closest occurrence of that character."""

    pattern_length = len(pattern)
    bad_character_table = { 0: {} }

    for available_char in available_characters:
        bad_character_table[0][available_char] = 0

    for i in reversed(range(0, pattern_length)):
        bad_character_table[i] = {}
        sub_pattern = pattern[0:i]
        sub_pattern_length = len(sub_pattern)

        for available_char in available_characters:
            pattern_char_found = False

            index = sub_pattern_length - 1
            while index >= 0:
                if available_char == sub_pattern[index]:
                    bad_character_table[i][available_char] = sub_pattern_length - index
                    pattern_char_found = True
                    break

                index -= 1

            if not pattern_char_found:
                bad_character_table[i][available_char] = 0

    return bad_character_table

def calculate_good_suffix_table(pattern,
                                available_characters):
    """Calculate the good suffix table.

    The table shoud have the amount of shift for each substring
    from the end back to the beginning to get a similar subpattern
    in the pattern."""

    pattern_length = len(pattern)
    good_suffix_table = { 0: 0 }

    for i in range(0, pattern_length + 1):
        subpattern = pattern[pattern_length - i:]
        subpattern_length = len(subpattern)

        # Special case for subpattern == ''
        if subpattern == "":
            good_suffix_table[pattern_length - i] = 0
            continue

        pattern_index = pattern_length - i - 1
        while (pattern[pattern_index:pattern_index + subpattern_length] !=
               subpattern and pattern_index >= 0):
            pattern_index -= 1

        if pattern_index > -1:
            good_suffix_table[pattern_length - i] = pattern_length - pattern_index - subpattern_length
        else:
            good_suffix_table[pattern_length - i] = 0

    return good_suffix_table

def match_pattern_boyer_moore(pattern, text):
    """Matches patterns using the Boyer-Moore algorithm.

    The Booyer More Algorithm uses two heuristics to determine where to
    jump to, the bad character heuristic and the good suffix heuristic. The
    precalculated jump amount for each of the two heuristics is looked up
    and then we jump backwards by the maximum number of characters as
    indicated.

    The Boyer Moore Algorithm can work better in
    certain cases where you have fewer repeated characters and unique
    substrings, but it generally gets more complex the longer your pattern
    (as compared to the length of the candidate text to be matched) because
    of the overhead of constructing the heuristics

    Characters are compared from P[len(p)] -> P[0].
    """

    matches = []

    text_length = len(text)
    pattern_length = len(pattern)

    available_characters = frozenset(text)

    good_suffix_table = calculate_good_suffix_table(pattern,
                                                    available_characters)
    bad_character_table = calculate_bad_character_table(pattern,
                                                        available_characters)        

    def _increment_backward_match_ptr(match_backwards_from, jump):
        match_backwards_from += jump
        if match_backwards_from > text_length - 1:
            match_backwards_from = text_length - 1

        return match_backwards_from

    match_backwards_from = pattern_length - 1
    while match_backwards_from <= text_length:
        on_last_character = (match_backwards_from == text_length - 1)

        for backwards_offset_index, pattern_index in enumerate(reversed(range(0, pattern_length))):

            # Mismatch case - look up in bad character table to see how far
            # we should jump forward (eg, so that we have the same number
            # of characters until the bad character would match again).
            #
            # If there isn't an entry, just jump forward the full amount
            if pattern[pattern_index] != text[match_backwards_from - backwards_offset_index]:
                if bad_character_table[pattern_index][text[match_backwards_from - backwards_offset_index]]:
                    jump = bad_character_table[pattern_index][text[match_backwards_from - backwards_offset_index]]
                else:
                    jump = pattern_length

                # Increment by j
                match_backwards_from = _increment_backward_match_ptr(match_backwards_from, jump)
                break

            # Match case - look up in good suffix index to see how far forward
            # we should jump so that we reach the same character again in
            # at the start of the pattern
            elif pattern_index == 0:
                if good_suffix_table[(pattern_length - 1) - pattern_index] > 0:
                    jump = good_suffix_table[(pattern_length - 1) - pattern_index]
                else:
                    jump = pattern_length

                matches.append(match_backwards_from - (pattern_length - 1))
                match_backwards_from = _increment_backward_match_ptr(match_backwards_from, jump)

        if on_last_character:
            break

    return matches
