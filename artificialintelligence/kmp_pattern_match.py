# /tests/kmp_pattern_match.py
#
# Pattern match using the Knuth method to optimize the outer loop
#
# See LICENCE.md for Copyright information
"""Knuth pattern matching method."""

def match_pattern_kmp(pattern, text):
    """Matches patterns using the KMP algorithm.

    The KMP algorithm mimics a finite-state-automata, jumping back a
    certain amount when we hit certain characters. This allows us to skip
    certain parts of the inner loop when we hit a recognizable sub-pattern.

    First we construct a prefix function and a table of prefixes for known
    steps into the pattern. The value of the prefix function is the longest
    subsequence of the suffix of pattern which is also a prefix of pattern.

    Then we use the prefix value as calculated during matches to jump ahead
    during pattern matching."""

    matches = []

    text_length = len(text)
    pattern_length = len(pattern)


    # This could probably be a recursive-descent type function, but it
    # isn't for now.
    def calculate_prefix(pattern, length):
        """Calculates the prefix value.

        Calculates the longest number of characters in the available prefixes
        which are also available in the pattern suffix for length number of
        characters in."""

        sub_pattern = pattern[0:length]
        prefixes = []

        for i in range(1, length):
            prefixes.append(pattern[0:i])

        highest_prefix_value = 0

        for prefix in prefixes:
            prefix_len = len(prefix)
            candidate_suffix = sub_pattern[length - prefix_len:]
            if candidate_suffix == prefix:
                highest_prefix_value = max(highest_prefix_value, prefix_len)

        return highest_prefix_value

    prefix_table = { 0: 0 }
    for i in range(1, pattern_length + 1):
        prefix_table[i] = calculate_prefix(pattern, i)

    pattern_index = 0
    string_index = 0

    # Attempt to match the length of the pattern
    while string_index - pattern_index <= text_length - pattern_length:
        if text[string_index + pattern_index] == pattern[pattern_index]:
            pattern_index += 1

            # Terminating condition - we've matched every character
            # in the pattern
            if pattern_index == pattern_length:
                matches.append(string_index)

                # Due to the prefix/suffix overlap, assume we've matched
                # n characters as precomputed in the prefix_table.
                pattern_index = prefix_table[pattern_index]

                # Movement of the string index is by the entire length
                # of the pattern (since we matched the whole thing), though
                # like below we roll-back to account for already-matched
                # characters
                string_index = string_index + pattern_length - pattern_index
        else:
            # Move by the number of chars we've checked so far
            move = pattern_index + 1

            # Next pattern_index (eg, we assume we've checked this many
            # characters already at this point due to the overlap)
            pattern_index = prefix_table[pattern_index]
            string_index = string_index + move - pattern_index

    return matches
