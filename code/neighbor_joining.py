import numpy as np
from distance_calculations import neighbor_joining_criterion


def best_hits(nodes):
    best_hits = {}
    return best_hits


def top_hits(total_nodes, n):
    seed_nodes = list(total_nodes.values())
    m = int(np.sqrt(n))
    while len(seed_nodes) > m:
        single_seed_node = seed_nodes[np.random.randint(0, len(seed_nodes))]
        seed_nodes.remove(single_seed_node)
        close_neighbors = calculate_close_neighbors(single_seed_node, seed_nodes, m)
        # It was unclear from the paper whether the top hits from the seed sequence should be
        # directly saved and the seed sequence should be removed from seed_nodes
        total_nodes[single_seed_node.get_label()].set_top_hits(close_neighbors)

        top_hits_helper = calculate_close_neighbors(single_seed_node, seed_nodes, 2 * m)
        for neighbor in close_neighbors:
            top_hits_helper_neighbor = top_hits_helper.copy()
            top_hits_helper_neighbor.remove(neighbor)
            total_nodes[neighbor.get_label()].set_top_hits(calculate_close_neighbors(neighbor, top_hits_helper_neighbor, m))
            seed_nodes.remove(neighbor)
    for remaining_sequence in seed_nodes:
        top_hits_sequences = seed_nodes.copy()
        top_hits_sequences.remove(remaining_sequence)
        total_nodes[remaining_sequence.get_label()].set_top_hits(top_hits_sequences)


def calculate_close_neighbors(seed, nodes, m):
    if len(nodes) < m:
        m = len(nodes)
    distances = []
    for i in range(len(nodes)):
        distances.append(neighbor_joining_criterion(seed, nodes[i], nodes))
    sorted_distances = distances.copy()
    sorted_distances.sort()
    m_distance = sorted_distances[m - 1]
    return [nodes[i] for i in range(len(nodes)) if distances[i] <= m_distance]
