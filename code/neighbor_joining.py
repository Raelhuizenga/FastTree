import numpy as np
from distance_calculations import neighbor_joining_criterion


def best_hits(nodes):
    best_hits_list = []
    for label, node in nodes.items():
        best_hit_dist = min(list(node.get_top_hits().values()))
        best_hit_label = [key for key, dist in node.get_top_hits().items() if dist == best_hit_dist][0]
        best_hits_list.append((label, best_hit_label, best_hit_dist))
    m = int(len(nodes)**0.5)
    best_hits_list = sorted(best_hits_list, key=lambda x: x[2])
    return best_hits_list[0:m]


def top_hits(total_nodes, n):
    """
    Calculates the top hits for each node in total_nodes and updates this in each node.
    :param total_nodes: dictionary with as key the label name and as value the node
    :type total_nodes: dict(str, Node)
    :param n: number of sequences
    :type n: int
    :return: None
    """
    seed_nodes = total_nodes.copy()
    m = int(np.sqrt(n))
    while len(seed_nodes) > m:
        single_seed_node = list(seed_nodes.keys())[np.random.randint(0, len(seed_nodes))]
        seed_node_value = seed_nodes.pop(single_seed_node)
        close_neighbors = calculate_close_neighbors(seed_node_value, seed_nodes, m, total_nodes)
        # It was unclear from the paper whether the top hits from the seed sequence should be
        # directly saved and the seed sequence should be removed from seed_nodes
        total_nodes[seed_node_value.get_label()].set_top_hits(close_neighbors)

        top_hits_helper = calculate_top_hits_helper(seed_node_value, seed_nodes, 2 * m, total_nodes)
        for neighbor in list(close_neighbors.keys()):
            top_hits_helper_neighbor = top_hits_helper.copy()
            top_hits_helper_neighbor.pop(neighbor)
            neighbor_value = seed_nodes[neighbor]
            total_nodes[neighbor].set_top_hits(calculate_close_neighbors(neighbor_value, top_hits_helper_neighbor, m, total_nodes))
            seed_nodes.pop(neighbor)
    for label, remaining_sequence in seed_nodes.items():
        top_hits_sequences = seed_nodes.copy()
        top_hits_sequences.pop(label)
        total_nodes[label].set_top_hits(calculate_close_neighbors(remaining_sequence, top_hits_sequences, len(top_hits_sequences), total_nodes))


def calculate_close_neighbors(seed, nodes, m, total_nodes):
    """
    Calculates the m closest neighbors of seed in nodes.
    :param seed: a node
    :type seed: Node
    :param nodes: the nodes to search in
    :type nodes: dict (string, Node)
    :param m: the number of neighbors to return
    :type m: int
    :return: the m closest neighbors of seed in nodes and the neighbor joining criterion value
    :rtype: dict (Node, float)
    """
    if len(nodes) < m:
        m = len(nodes)
    distances = []
    for label, distance in nodes.items():
        distances.append(neighbor_joining_criterion(seed, total_nodes[label], nodes))
    sorted_distances = distances.copy()
    sorted_distances.sort()
    m_distance = sorted_distances[m - 1]
    close_neighbors = {}
    for i, label in enumerate(list(nodes.keys())):
        if distances[i] <= m_distance:
            close_neighbors[label] = distances[i]
    return close_neighbors

def calculate_top_hits_helper(seed, nodes, m, total_nodes):
    """
    Calculates the m closest neighbors of seed in nodes.
    :param seed: a node
    :type seed: Node
    :param nodes: the nodes to search in
    :type nodes: dict (string, Node)
    :param m: the number of neighbors to return
    :type m: int
    :return: the m closest neighbors of seed in nodes and the neighbor joining criterion value
    :rtype: dict (Node, float)
    """
    if len(nodes) < m:
        m = len(nodes)
    distances = []
    for label, distance in nodes.items():
        distances.append(neighbor_joining_criterion(seed, total_nodes[label], nodes))
    sorted_distances = distances.copy()
    sorted_distances.sort()
    m_distance = sorted_distances[m - 1]
    close_neighbors = {}
    for i, label in enumerate(list(nodes.keys())):
        if distances[i] <= m_distance:
            close_neighbors[label] = nodes[label]
    return close_neighbors
