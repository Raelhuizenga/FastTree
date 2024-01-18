import math
from distance_calculations import log_corrected_profile_distance
from profile_creation import create_combined_profile
from node import Node


def run_nearest_neighbor_interchanges(n, root_node):
    """
    Runs the nearest neighbor interchanges algorithm on the tree.
    :param n: the number of sequences (= number of leaves)
    :type n: int
    :param root_node: the root node of the tree
    :type root_node: Node
    """
    max_iter = round(math.log(n)) + 1
    for i in range(max_iter):
        post_order_list = post_order_traversal(root_node, [])
        list_is_changed = False
        for node_f1, node_f2 in post_order_list:
            node_a, node_b, node_c, node_d = get_nodes_to_possibly_rearrange(node_f1, node_f2)
            if nearest_neighbor_interchange(node_a, node_b, node_c, node_d):
                list_is_changed = True
                break
        if not list_is_changed:
            break


def post_order_traversal(node, post_order_list):
    """
    Performs a post order traversal of the tree.
    :param node: the node to start the traversal from
    :type node: Node
    :param post_order_list: the list of nodes in post order
    :type post_order_list: list[(Node, Node)]
    :return: the complete list of nodes in post order
    :rtype: list[(Node, Node)]
    """
    if node.get_children():
        post_order_traversal(node.get_children()[0], post_order_list)
        post_order_traversal(node.get_children()[1], post_order_list)
        possible_f2 = node.get_parent()
        if possible_f2:
            if possible_f2.get_parent():
                post_order_list.append((node, possible_f2))
    return post_order_list


def get_nodes_to_possibly_rearrange(neighbor_node_1, neighbor_node_2):
    """
    Gets the nodes that can be rearranged.
    :param neighbor_node_1: the first neighbor node
    :type neighbor_node_1: Node
    :param neighbor_node_2: the second neighbor node
    :type neighbor_node_2: Node
    :return: the nodes that can be rearranged
    :rtype: (Node, Node, Node, Node)
    """
    node_a = neighbor_node_1.get_children()[0]
    node_b = neighbor_node_1.get_children()[1]
    node_c = neighbor_node_2.get_children()[1]
    if node_c == neighbor_node_1:
        node_c = neighbor_node_2.get_children()[0]
    node_d = neighbor_node_2.get_parent()
    return node_a, node_b, node_c, node_d


def nearest_neighbor_interchange(node_a, node_b, node_c, node_d):
    """
    Calculates distances and performs a nearest neighbor interchange on the given nodes if needed.
    :param node_a: the first node
    :type node_a: Node
    :param node_b: the second node
    :type node_b: Node
    :param node_c: the third node
    :type node_c: Node
    :param node_d: the fourth node
    :type node_d: Node
    """
    dist_1 = log_corrected_profile_distance(node_a, node_b) + log_corrected_profile_distance(node_c, node_d)
    dist_2 = log_corrected_profile_distance(node_a, node_c) + log_corrected_profile_distance(node_b, node_d)
    dist_3 = log_corrected_profile_distance(node_b, node_c) + log_corrected_profile_distance(node_a, node_d)
    if dist_1 < dist_2 and dist_1 < dist_3:
        f_1 = node_a.get_parent()
        f_2 = node_c.get_parent()
        # Question: How can the new profiles change?
        # Should we recompute lambda to do this?
        # How can we do this if we do not have any active nodes?
        f_1.set_profile(create_combined_profile(node_a, node_b, f_1.get_lambda()))
        f_2.set_profile(create_combined_profile(node_c, f_1, f_2.get_lambda()))
        return False
    if dist_2 < dist_3:
        change_to_topology_2(node_a, node_b, node_c, node_d)
        return True
    else:
        change_to_topology_3(node_a, node_b, node_c, node_d)
        return True


def change_to_topology_2(node_a, node_b, node_c, node_d):
    """
    Changes the topology of the tree to the topology of dist2.
    :param node_a: the first node
    :type node_a: Node
    :param node_b: the second node
    :type node_b: Node
    :param node_c: the third node
    :type node_c: Node
    :param node_d: the fourth node
    :type node_d: Node
    """
    f_1 = node_a.get_parent()
    f_2 = node_c.get_parent()
    f_1.set_children([node_a, node_c])
    f_2.set_children([node_b, f_1])
    node_c.set_parent(f_1)
    node_b.set_parent(f_2)
    # Question: what lamda should we use here?
    f_1.set_profile(create_combined_profile(node_a, node_c, f_1.get_lambda()))
    f_2.set_profile(create_combined_profile(node_b, f_1, f_2.get_lambda()))


def change_to_topology_3(node_a, node_b, node_c, node_d):
    """
    Changes the topology of the tree to the topology of dist3.
    :param node_a: the first node
    :type node_a: Node
    :param node_b: the second node
    :type node_b: Node
    :param node_c: the third node
    :type node_c: Node
    :param node_d: the fourth node
    :type node_d: Node
    """
    f_1 = node_a.get_parent()
    f_2 = node_c.get_parent()
    f_1.set_children([node_b, node_c])
    f_2.set_children([node_a, f_1])
    node_c.set_parent(f_1)
    node_a.set_parent(f_2)
    # Question: what lamda should we use here?
    f_1.set_profile(create_combined_profile(node_b, node_c, f_1.get_lambda()))
    f_2.set_profile(create_combined_profile(node_a, f_1, f_2.get_lambda()))
