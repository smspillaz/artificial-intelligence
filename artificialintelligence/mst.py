# /artificialintelligence/mst.py
#
# Finds a minimum spanning tree for an input sparse matrix.
#
# See LICENCE.md for Copyright information
"""Finds a minimum spanning tree for a sparse matrix."""

from collections import namedtuple

class DisjointSet(object):

    """A disjoint set.

    This contains a number of subsets of elements. It exposes two main
    operations, that being find(), which tells you which set-id an element
    resides in, and merge(a, b), which merges the two sets which contain
    items a and b."""

    def __init__(self, starting_elements):
        """Create new disjoint set with a set for elem in starting_elements."""

        super(DisjointSet, self).__init__()

        self._sets = [frozenset([e]) for e in starting_elements]

    def find(self, element):
        """Return the index of the set which contains this element."""

        for set_id in range(0, len(self._sets)):
            if element in self._sets[set_id]:
                return set_id

        raise KeyError("Unable to find element {0} in sets".format(element))

    def merge(self, element_a, element_b):
        """Merges the two sets containing element_a and element_b."""

        first_set_index = self.find(element_a)
        second_set_index = self.find(element_b)

        if first_set_index == second_set_index:
            raise ValueError("Element {0} is in the same"
                             " set as {1}".format(element_a, element_b))

        merged_set = self._sets[first_set_index] | self._sets[second_set_index]
        del_ind = [first_set_index, second_set_index]

        self._sets = [i for j, i in enumerate(self._sets) if j not in del_ind]
        self._sets.append(merged_set)

Edge = namedtuple("Edge", "vertex_one vertex_two weight")


def minimum_spanning_tree(undirected_graph):
    """Create a minimum spanning tree from undirected_graph.

    The undirected_graph takes the form of a compressed sparse matrix, where
    each row representes a node and each column represents the weight of a
    connection to another node.

    So for instance, a graph that looks like this:

    (0)--3-(1)---2--(2)--4-(3)
      \     /         \     /
       1   5           7   2
        \ /             \ /
        (4)------4------(5)
         \               /
          \             /
           \           /
            \         /
             6       9
              \     /
               \   /
                (6)
    
    Will take the following form:

    [
        [ 0, 3, 0, 0, 1, 0, 0 ],
        [ 3, 0, 0, 0, 5, 0, 0 ],
        [ 0, 2, 0, 4, 0, 7, 0 ],
        [ 0, 0, 4, 0, 0, 2, 0 ],
        [ 1, 5, 0, 0, 0, 4, 6 ],
        [ 0, 0, 7, 2, 4, 0, 9 ],
        [ 0, 0, 0, 0, 6, 9, 0 ]
    ].

    The output will be the minimum_spanning_tree as computed by the Kruskal
    algorithm. This is the tree connects all the nodes togther by the minimum
    weight.

    It works by putting each node into a disjoint set and then sorting each
    edge by its weight. An edge is taken if both of its nodes are not part
    of the same set. When an edge is taken, both of the sets its nodes belong
    to are merged. This prevents cycles.

    Once we have all the edges, we then compute a sparse matrix representation
    of all the connections between the nodes."""

    undirected_graph_len = len(undirected_graph)

    # Sanity check
    for row in undirected_graph:
        assert len(row) == len(undirected_graph[0])
        assert len(row) == len(undirected_graph)

    edges = []

    for node_index in range(0, undirected_graph_len):
        for connecting_index in range(0, undirected_graph_len):
            distance = undirected_graph[node_index][connecting_index]
            if distance != 0:
                # Check for inverse edges which might already form a part
                # of our edge list.
                if not Edge(connecting_index, node_index, distance) in edges:
                    edges.append(Edge(vertex_one=node_index,
                                      vertex_two=connecting_index,
                                      weight=distance))

    disjoint_set_of_nodes = DisjointSet(range(0, undirected_graph_len))
    minimum_spanning_tree_edges = []

    # Start merging the sets and adding edges as appropriate.
    for edge in sorted(edges, key=lambda e: e.weight):
        if (disjoint_set_of_nodes.find(edge.vertex_one) !=
            disjoint_set_of_nodes.find(edge.vertex_two)):
            disjoint_set_of_nodes.merge(edge.vertex_one, edge.vertex_two)
            minimum_spanning_tree_edges.append(edge)

    mst_csr_row = [0 for i in range(0, undirected_graph_len)]
    mst_csr = [mst_csr_row[:] for i in range(0, undirected_graph_len)]

    for edge in minimum_spanning_tree_edges:
        mst_csr[edge.vertex_one][edge.vertex_two] = edge.weight

    return mst_csr

