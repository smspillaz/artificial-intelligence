# /tests/insert_sort.py
#
# Simple insert 
#
# See LICENCE.md for Copyright information
"""Loader module."""

from collections import defaultdict

import sys

def knapsack(items, capacity):
    """0-1 knapsack dynamic programming algorithm."""

    table = defaultdict(dict)

    for i in range(0, capacity + 1):
        table[i][0] = 0

    def value(item_number, current_capacity):
        """Calculates the value for this capacity/weight combination."""

        try:
            return table[current_capacity][item_number]
        except KeyError:
            item_index = item_number - 1

            if item_number == 0:
                current_value = 0

            # We can pick up this item - add it to our values and deduct from
            # our capacity
            elif current_capacity - items[item_index].cost >=0:

                # Fork here - do one set of recursions without adding this item
                # and do one set of recursions whilst adding this value
                current_value = max((value(item_number - 1,
                                           current_capacity - items[item_index].cost) +
                                           items[item_index].value), # add item
                                    value(item_number - 1, # don't add item
                                           current_capacity))
            else:
                current_value = value(max(0, item_number - 1), current_capacity)

            print("Set {0}:{1} to {2}".format(current_capacity, item_number, current_value))
            table[current_capacity][item_number] = current_value
            return current_value

    retval = value(len(items), capacity)

    # Fill in the rest of the table ... copy values from the lower
    # row if there's no value in the upper row:
    for j in range(0, capacity):
        for i in reversed(range(0, len(items) + 1)):
            try:
                table[j][i]
            except KeyError:
                try:
                    table[j][i] = table[j][max(i + 1, len(items) - 1)]
                except KeyError:
                    table[j][i] = 0


    return (table, retval)

def _print_table(table, num_items):
    """Prints the table."""

    sys.stdout.write("   {0}".format('  '.join([str(i) for i in table.keys()])))
    sys.stdout.write("\n")

    for index in range(0, num_items):
        sys.stdout.write("{0}".format(index))
        sys.stdout.write("  {0}\n".format('  '.join([str(table[i][index]) for i in table.keys()])))


def items_for_knapsack(items, capacity):
    """Returns the optimal items that make up the knapsack with capacity."""

    table, retval = knapsack(items, capacity)

    _print_table(table, len(items) + 1)

    def pick_items(count, capacity, value):
        """Picks items and returns them (recursively)."""

        # Base case
        if count == 0:
            return []

        if (value ==
            table[capacity][count - 1]):
            return pick_items(count - 1,
                              capacity,
                              value)
        else:
            return pick_items(count - 1,
                              capacity - items[count - 1].cost,
                              value - items[count - 1].value) + [items[count - 1].value]


    return pick_items(len(items), capacity, retval)
