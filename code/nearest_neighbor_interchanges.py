from distance_calculations import log_corrected_profile_distance
from profile_creation import create_combined_profile
from node import Node


def get_nodes_to_possibly_rearrange(neighbor_node_1, neighbor_node_2):
    pass


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
    dist_1 = log_corrected_profile_distance(node_a.get_profile(), node_b.get_profile()) + log_corrected_profile_distance(node_c.get_profile(), node_d.get_profile())
    dist_2 = log_corrected_profile_distance(node_a.get_profile(), node_c.get_profile()) + log_corrected_profile_distance(node_b.get_profile(), node_d.get_profile())
    dist_3 = log_corrected_profile_distance(node_b.get_profile(), node_c.get_profile()) + log_corrected_profile_distance(node_a.get_profile(), node_d.get_profile())
    if dist_1 < dist_2 and dist_1 < dist_3:
        return
    if dist_2 < dist_3:
        change_to_topology_2(node_a, node_b, node_c, node_d)
        return
    else:
        # change topology to dist3 topology
        return


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
    f_2.set_children([node_b, node_d])
    node_c.set_parent(f_1)
    node_d.set_parent(f_2)
    f_1.set_profile(create_combined_profile(node_a, node_c))
    f_2.set_profile(create_combined_profile(node_b, node_d))


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
    f_2.set_children([node_a, node_d])
    node_c.set_parent(f_1)
    node_a.set_parent(f_2)
    f_1.set_profile(create_combined_profile(node_b, node_c))
    f_2.set_profile(create_combined_profile(node_a, node_d))
