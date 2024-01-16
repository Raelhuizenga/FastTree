import numpy as np
from distance_calculations import neighbor_joining_criterion, up_distance
from node import Node
from profile_creation import create_combined_profile
from get_active_nodes import get_active_nodes


def best_hits(nodes):
    """
    Calculates the best hits list consisting of the best hit of each node.
    :param nodes: dictionary with as key the label name and as value the node
    :type nodes: dict(str, Node)
    :return: list with m tuples (startnode_label, endnode_label, distance)
    :rtype: list[tuple(str, str, float)]
    """
    best_hits_list = []
    active_nodes = get_active_nodes(nodes)
    for label, node in active_nodes.items():
        best_hit_dist = min(list(node.get_top_hits().values()))
        best_hit_label = [key for key, dist in node.get_top_hits().items() if dist == best_hit_dist][0]
        best_hits_list.append((label, best_hit_label, best_hit_dist))
    m = int(len(active_nodes)**0.5)
    best_hits_list = sorted(best_hits_list, key=lambda x: x[2])
    return best_hits_list[0:m]


def get_best_hit(best_hit_list, all_nodes):
    """"
    Calculates the best hit from the best hits list by recomputing the neighbor joining criterion.
    :param best_hit_list: list with m tuples (startnode_label, endnode_label, distance)
    :type best_hit_list: list[tuple(str, str, float)]
    :param all_nodes: dictionary with as key the label name and as value the node
    :type all_nodes: dict(str, Node)
    :return: the best hit from the best hits list
    :rtype: tuple(str, str)
    """
    distance, best_join = float('inf'), None
    for item in best_hit_list:
        new_distance = neighbor_joining_criterion(all_nodes[item[0]], all_nodes[item[1]], all_nodes)
        if new_distance < distance:
            best_join = item
            distance = new_distance
    return best_join[0], best_join[1]


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

        top_hits_helper = calculate_close_neighbors(seed_node_value, seed_nodes, 2 * m, total_nodes)
        #TODO: check if seed should be part of top_hits_helper (now it isnt)
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
    :type nodes: dict(str, Node)
    :param m: the number of neighbors to return
    :type m: int
    :return: the labels of the m closest neighbors of seed in nodes and their distance
    :rtype: dict(str, float)
    """
    nodes_without_seed = nodes.copy()
    if seed.get_label() in nodes_without_seed:
        del nodes_without_seed[seed.get_label()]
    if len(nodes_without_seed) < m:
        m = len(nodes_without_seed)
    distances = []
    for label, distance in nodes_without_seed.items():
        distances.append(neighbor_joining_criterion(seed, total_nodes[label], total_nodes))
    sorted_distances = distances.copy()
    sorted_distances.sort()
    m_distance = sorted_distances[m - 1]
    close_neighbors = {}
    for i, label in enumerate(list(nodes_without_seed.keys())):
        if distances[i] <= m_distance:
            close_neighbors[label] = distances[i]
    return close_neighbors


def remove_lineage_from_top_hits(node_1, top_hits_list_2):
    '''
    Removes the lineage of node_1 from the top hits list of node_2.
    :param node_1: the node to remove the lineage of
    :type node_1: Node
    :param top_hits_list_2: the top hits list to remove the lineage from
    :type top_hits_list_2: dict(str, float)
    :return: None
    '''
    if node_1.get_label() in top_hits_list_2:
        del top_hits_list_2[node_1.get_label()]
    if node_1.get_children():
        remove_lineage_from_top_hits(node_1.get_children()[0], top_hits_list_2)
        remove_lineage_from_top_hits(node_1.get_children()[1], top_hits_list_2)


def merge_top_hits_list(node_1, node_2, m, merged_node, all_nodes):
    '''
    Merges the top hits list of node_1 and node_2 into the top hits list of merged_node.
    :param node_1: the first node to merge
    :type node_1: Node
    :param node_2: the second node to merge
    :type node_2: Node
    :param m: the number of neighbors to return
    :type m: int
    :param merged_node: the node to merge the top hits list into
    :type merged_node: Node
    :param all_nodes: all nodes
    :type all_nodes: dict(str, Node)
    :return: None
    '''
    top_hits_list_1 = node_1.get_top_hits().copy()
    top_hits_list_2 = node_2.get_top_hits().copy()
    remove_lineage_from_top_hits(node_1, top_hits_list_2)
    remove_lineage_from_top_hits(node_2, top_hits_list_1)
    for key, value in top_hits_list_1.items():
        if key in top_hits_list_2:
            if top_hits_list_2[key] < value:
                top_hits_list_1[key] = top_hits_list_2[key]
            del top_hits_list_2[key]
    top_hits_list_1.update(top_hits_list_2)

    if len(top_hits_list_1) > 0.8 * m and len(top_hits_list_1) > 1:
        if len(top_hits_list_1) <= m:
            merged_node.set_top_hits(top_hits_list_1)
            return
        distances = list(top_hits_list_1.values())
        distances = sorted(distances)
        m_distance = distances[m-1]
        top_hits_list_1_copy = top_hits_list_1.copy()
        for key, value in top_hits_list_1_copy.items():
            if value > m_distance:
                del top_hits_list_1[key]
    else:
        update_top_hits(merged_node, all_nodes)
        return
    merged_node.set_top_hits(top_hits_list_1)
    return


def update_top_hits(node_to_update, all_nodes):
    '''
    Updates the top hits list of node_to_update.
    :param node_to_update: the node to update the top hits list of
    :type node_to_update: Node
    :param all_nodes: all nodes
    :type all_nodes: dict(str, Node)
    :return: None
    '''
    active_nodes = get_active_nodes(all_nodes)
    m = int(len(active_nodes)**(1/2))
    new_top_hits = calculate_close_neighbors(node_to_update, active_nodes, m, all_nodes)
    node_to_update.set_top_hits(new_top_hits)
    top_hits_helper = calculate_close_neighbors(node_to_update, active_nodes, 2*m, all_nodes)
    # @ToDo merge old top hits list with new top hits list??
    for close_neighbor, distance in new_top_hits.items():
        top_hits_list = calculate_close_neighbors(all_nodes[close_neighbor], top_hits_helper, m, all_nodes)
        all_nodes[close_neighbor].set_top_hits(top_hits_list)


def create_join(best_hit, all_nodes, update_top_hits=True):
    '''
    Creates a join between the two nodes in best_hit.
    :param best_hit: the best hit to join
    :type best_hit: tuple(str, str)
    :param all_nodes: all nodes
    :type all_nodes: dict(str, Node)
    :param update_top_hits: if the top hits list should be updated
    :type update_top_hits: boolean
    :return: None
    '''
    node_1 = all_nodes[best_hit[0]]
    node_2 = all_nodes[best_hit[1]]
    age = max(node_1.get_age(), node_2.get_age()) + 1
    new_profile = create_combined_profile(node_1, node_2)
    updistance = up_distance(node_1.get_profile(), node_2.get_profile())
    new_label = node_1.get_label() + node_2.get_label()
    joined_node = Node(age, new_profile, {}, updistance, new_label, [node_1, node_2], True, None)
    all_nodes[new_label] = joined_node
    node_1.set_active(False)
    node_2.set_active(False)
    node_1.set_parent(joined_node)
    node_2.set_parent(joined_node)
    if update_top_hits:
        m = int(len(get_active_nodes(all_nodes)) ** (1 / 2))
        merge_top_hits_list(node_1, node_2, m, joined_node, all_nodes)



