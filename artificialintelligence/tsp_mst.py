# /artificialintelligence/tsp_mst.py
#
# Implementation of the Travelling Salesman Problem using minimum
# spanning trees
#
# See LICENCE.md for Copyright information
"""Loader module."""

from artificialintelligence.mst import minimum_spanning_tree

from collections import namedtuple

import math

MSTNode = namedtuple("MSTNode", "which distance")
TSPNode = namedtuple("TSPNode", "x y")

def _depth_first_search_recurse(current_node, mst_array, traversal, recursion):
    """Expand all the subnodes of this node

    We have to discover what those subnodes actually are."""

    nodes_to_expand = []
    path_part = []

    for i in range(0, len(mst_array[current_node])):
        if mst_array[current_node][i] != 0 and i not in traversal:
            nodes_to_expand.append(MSTNode(i,
                                           mst_array[current_node][i]))

    for i in range(0, len(mst_array)):
        if mst_array[i][current_node] != 0 and i not in traversal:
            nodes_to_expand.append(MSTNode(i,
                                           mst_array[i][current_node]))

    for node in sorted(frozenset(nodes_to_expand), key=lambda n: n.distance):
        path_part.append(node)
        path_part += _depth_first_search_recurse(node.which,
                                                 mst_array,
                                                 traversal + [node.which],
                                                 recursion + 1)

    return path_part

def depth_first_search(current_node, mst_array):
    """Perform a depth first search of a minimum spanning tree.

    The tree must be in sparse representation."""

    return [MSTNode(current_node, 0)] + _depth_first_search_recurse(current_node,
                                                                    mst_array,
                                                                    [current_node],
                                                                    0)



def _find_tsp_path_from_distances(undirected_graph, start_index):
    """Finds a path for an undirected graph in the a csr matrix form.

    undirected_graph must be in the following form:

    [
        [ v(0,0), v(0, 1), v(0, 2), v(0, 3) ],
        [ v(1,0), v(1, 1), v(1, 2), v(1, 3) ],
        [ v(2,0), v(2, 1), v(2, 2), v(2, 3) ],
        [ v(3,0), v(3, 1), v(3, 2), v(3, 3) ]
    ]

    If v(i, j) and v(j, i) are both zero, then there is no connection
    between the two nodes. If one of them is nonzero, then the distance
    between the two is the highest value of either of them.

    So for instance:

    [
        [ 0, 8, 0, 3 ],
        [ 8, 0, 2, 5 ],
        [ 0, 2, 0, 6 ],
        [ 3, 5, 6, 0 ]
    ]

    MSTNode 0 is connected to node 0 by nothing (eg, cannot connect to itself)
    MSTNode 0 is connected to node 1 by 8 (csr[0][1] == csr[1][0] == 8)
    MSTNode 0 is connected to node 2 by 0 (no connection)
    MSTNode 0 is connected to node 3 by 3 (csr[0][3] == csr[3][0] == 3)

    MSTNode 3 is connected to node 0 by 3 (csr[0][3] == csr[3][0] == 3)
    MSTNode 3 is connected to node 1 by 5 (csr[1][3] == csr[3][1] == 5)
    MSTNode 3 is connected to node 2 by 6 (csr[2][3] == csr[3][2] == 6)
    MSTNode 3 is connected to node 3 by zero (cannot connect to itself).

    The output graph is in the same form, (but it only shows the minimum
    spanning tree and not all the connections).
    """

    for i in range(0, len(undirected_graph)):
        assert len(undirected_graph[i]) == len(undirected_graph[0])

    mst_array = minimum_spanning_tree(undirected_graph)
    path = depth_first_search(start_index, mst_array)

    return path

def find_tsp_path(cities, start_index):
    """Finds a travelling-salesman-path from a bunch of cities.

    First we need to take our list of cities and then construct a sparce-matrix
    undirected graph of cities with the distances between each of the vertices
    on the graph.

    Each city is given an index, and the matrix will be N x N large. Each
    column of the matrix is the distance from city i (the row) to city j
    (the column index).

    A distance of zero means that the city can't be reached from that one.

    So for instance, with a list of cities like this, you should get the
    following:

    - City(0, 3)
    - City(0, 1)
    - City(1, 1)

    [
        [ 0, 2, sqrt(pow(2, 2), pow(1, 2)) ],
        [ 2, 0, 1 ],
        [ sqrt(pow(2, 2), pow(1, 2)), 1, 0 ]
    ].

    After we have found that table, we use _find_tsp_path_from_distances to
    find a path from those distances which returns a list of MSTNodes. We
    then convert that path into the cities themselves by looking up the
    indicies on the nodes in the cities array."""

    distance_undirected_graph = []

    for city_row_index in range (0, len(cities)):
        row_graph = []

        for city_col_index in range(0, len(cities)):
            if city_col_index == city_row_index:
                row_graph.append(0)
            else:
                reference_city = cities[city_col_index]
                target_city = cities[city_row_index]

                row_graph.append(math.sqrt(math.pow(target_city.x -
                                                    reference_city.x, 2) +
                                           math.pow(target_city.y -
                                                    reference_city.y, 2)))

        distance_undirected_graph.append(row_graph)

    for row in distance_undirected_graph:
        assert len(row) == len(distance_undirected_graph)
        assert len(row) == len(distance_undirected_graph[0])

    mst_path = _find_tsp_path_from_distances(distance_undirected_graph,
                                             start_index)
    path = []

    for node in mst_path:
        path.append(cities[node.which])

    return path + [cities[start_index]]