from get_active_nodes import get_active_nodes
import math

def neighbor_joining_criterion(node_i, node_j, all_nodes):
    """
    Calculates the neighbor joining criterion for node_i and node_j.
    :param node_i: the first node
    :type node_i: Node
    :param node_j: the second node
    :type node_j: Node
    :param all_nodes: all nodes
    :type all_nodes: dict(label, node)
    :return: the neighbor joining criterion for node_i and node_j
    :rtype: float
    """
    active_nodes = get_active_nodes(all_nodes)
    return profile_distance(node_i.get_profile(), node_j.get_profile()) - node_i.get_up_distance() \
        - node_j.get_up_distance() - average_out_distance(node_i, active_nodes) - average_out_distance(node_j, active_nodes)


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
    if len(profile_i) != len(profile_j) or len(profile_i[0]) != len(profile_j[0]):
        raise ValueError('profiles not of the same size')
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
    :param active_nodes: the active nodes with their labels
    :type active_nodes: dict (str, Node)
    :return: the average out distance of node
    :rtype: float
    """
    dist = 0
    for label, active_node in active_nodes.items():
        dist += profile_distance(node.get_profile(), active_node.get_profile()) - node.get_up_distance() \
                - active_node.get_up_distance()
    return dist / (len(active_nodes) - 2)


def log_corrected_profile_distance(node_1, node_2, all_nodes):
    """
    Calculates the log corrected profile distance between two nodes.
    :param node_1: the first node
    :type node_1: Node
    :param node_2: the second node
    :type node_2: Node
    :param all_nodes: all nodes
    :type all_nodes: dict(label, node)
    :return: the log corrected profile distance between node_1 and node_2
    :rtype: float
    """
    profile_1 = all_nodes[node_1].get_profile()
    profile_2 = all_nodes[node_2].get_profile()
    d = profile_distance(profile_1, profile_2)
    return round(-(3/4) * math.log(1 - (4/3) * d) , 3)


def branch_length(node_1, node_2, all_nodes):
    '''
    Calculates the branch length between node_1 and node_2.
    :param node_1: the first node
    :type node_1: Node
    :param node_2: the second node
    :type node_2: Node
    :param all_nodes: all nodes
    :type all_nodes: dict(str, Node)
    :return: the branch length between node_1 and node_2
    :rtype: float
    '''
    if node_1.get_children() and node_2.get_children():
        A = node_1.get_children()[0].get_label()
        B = node_1.get_children()[1].get_label()
        C = node_2.get_children()[0].get_label()
        D = node_2.get_children()[1].get_label()
        return round((log_corrected_profile_distance(A,C,all_nodes) + log_corrected_profile_distance(A,D,all_nodes) + \
                log_corrected_profile_distance(B,C,all_nodes) + log_corrected_profile_distance(B, D, all_nodes))/4 \
                - (log_corrected_profile_distance(A, B, all_nodes) + log_corrected_profile_distance(C, D, all_nodes))/2, 3)
    elif node_1.get_children() and not node_2.get_children():
        A = node_1.get_children()[0].get_label()
        B = node_1.get_children()[1].get_label()
        C = node_2.get_label()
        return round((log_corrected_profile_distance(C, A, all_nodes)+log_corrected_profile_distance(C, B, all_nodes) - \
                log_corrected_profile_distance(A, B, all_nodes)) / 2, 3)
    elif not node_1.get_children() and node_2.get_children:
        A = node_1.get_label()
        B = node_2.get_children()[0].get_label()
        C = node_2.get_children()[1].get_label()
        return round((log_corrected_profile_distance(A, B, all_nodes)+log_corrected_profile_distance(A, C, all_nodes) - \
                log_corrected_profile_distance(B, C, all_nodes)) / 2, 3)
    else:
        A = node_1.get_label()
        B = node_2.get_label()
        return log_corrected_profile_distance(A, B, all_nodes)

