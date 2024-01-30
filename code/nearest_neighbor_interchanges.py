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
        # Make a new post order list every time,
        # because the order could have been changed by an interchange in the previous step.
        post_order_list = post_order_traversal(root_node, [])
        list_is_changed = False
        for node_f1, node_f2 in post_order_list:
            node_a, node_b, node_c, node_d = get_nodes_to_possibly_rearrange(node_f1, node_f2)
            if nearest_neighbor_interchange(node_a, node_b, node_c, node_d):
                list_is_changed = True
                break
        # If the list was not changed, we can stop the nearest neighbor interchanges.
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


def nni_lambda(node_a, node_b, node_c, node_d):
    return 1 / 2 + (log_corrected_profile_distance(node_b, node_c) + log_corrected_profile_distance(node_b,
                                                                                                    node_d) - log_corrected_profile_distance(
        node_a, node_c) - log_corrected_profile_distance(node_a, node_d)) / (
                4 * log_corrected_profile_distance(node_a, node_b))


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
    f_1 = node_a.get_parent()
    f_2 = node_c.get_parent()
    if dist_1 < dist_2 and dist_1 < dist_3:
        # The topology stays the same, but the combined profile could be different because we calculate a new lambda.
        f_1.set_profile(create_combined_profile(node_a, node_b, nni_lambda(node_a, node_b, node_c, node_d)))
        f_2.set_profile(create_combined_profile(node_c, f_1, nni_lambda(node_c, node_d, node_a, node_b)))
        return False
    if dist_2 < dist_3:
        # Switch node b and c
        change_to_different_topology(node_a, node_c, node_b, node_d, f_1, f_2)
        return True
    else:
        # Switch node a and c
        change_to_different_topology(node_b, node_c, node_a, node_d, f_1, f_2)
        return True


def change_to_different_topology(node_a, node_b, node_c, node_d, f_1, f_2):
    """
    Changes the topology of the tree to a topology where node a and b are children of f_1,
     and node c is child of node f_2.
    :param node_a: the node at the first position
    :type node_a: Node
    :param node_b: the node at the second position
    :type node_b: Node
    :param node_c: the node at the third position
    :type node_c: Node
    :param node_d: the node at the fourth position
    :type node_d: Node
    :param f_1: first parent node
    :type f_1: Node
    :param f_2: second parent node
    :type f_2: Node
    """
    f_1.set_children([node_a, node_b])
    f_2.set_children([node_c, f_1])
    node_b.set_parent(f_1)
    node_c.set_parent(f_2)
    f_1.set_profile(create_combined_profile(node_a, node_b, nni_lambda(node_a, node_b, node_c, node_d)))
    f_2.set_profile(create_combined_profile(node_c, f_1, nni_lambda(node_c, node_d, node_a, node_b)))
