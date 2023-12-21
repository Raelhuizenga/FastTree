def neighbor_joining_criterion(node_i, node_j, nodes):
    """
    Calculates the neighbor joining criterion for node_i and node_j.
    :param node_i: the first node
    :type node_i: Node
    :param node_j: the second node
    :type node_j: Node
    :param nodes: all nodes
    :type nodes: list[Node]
    :return: the neighbor joining criterion for node_i and node_j
    :rtype: float
    """
    return profile_distance(node_i.get_profile(), node_j.get_profile()) - node_i.get_up_distance() \
        - node_j.get_up_distance() - average_out_distance(node_i, nodes) - average_out_distance(node_j, nodes)


def hamming_distance(pattern_1, pattern_2):
    """
    Calculates the hamming distance between two patterns.
    :param pattern_1: the first pattern
    :type pattern_1: str
    :param pattern_2: the second pattern
    :type pattern_2: str
    :return: the hamming distance between pattern_1 and pattern_2
    :rtype: int
    """
    distance = 0
    for i in range(len(pattern_1)):
        if pattern_1[i] != pattern_2[i]:
            distance += 1
    return distance


# preprint paper page 11
def up_distance(profile_i, profile_j):
    """
    Calculates the up distance between two profiles.
    :param profile_i: the first profile
    :type profile_i: list[list[float]]
    :param profile_j: the second profile
    :type profile_j: list[list[float]]
    :return: the up distance between profile_i and profile_j
    :rtype: float
    """
    return profile_distance(profile_i, profile_j) / 2


# preprint paper page 3
def profile_distance(profile_i, profile_j):
    """
    Calculates the profile distance between two profiles.
    :param profile_i: the first profile
    :type profile_i: list[list[float]]
    :param profile_j: the second profile
    :type profile_j: list[list[float]]
    :return: the profile distance between profile_i and profile_j
    :rtype: float
    """
    profile_distance_value = 0
    for l in range(len(profile_i[0])):
        for a in range(4):
            for b in range(4):
                if a != b:
                    profile_distance_value += profile_i[a][l] * profile_j[b][l]
    profile_distance_value = profile_distance_value / len(profile_i[0])
    return profile_distance_value


def average_out_distance(node, active_nodes):
    """
    Calculates the average out distance of node.
    :param node: the node to calculate the average out distance of
    :type node: Node
    :param active_nodes: the active nodes
    :type active_nodes: dict (string, Node)
    :return: the average out distance of node
    :rtype: float
    """
    dist = 0
    for label, active_node in active_nodes.items():
        dist += profile_distance(node.get_profile(), active_node.get_profile()) - node.get_up_distance() \
                - active_node.get_up_distance()
    return dist / (len(active_nodes) - 2)
