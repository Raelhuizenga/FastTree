from distance_calculations import log_corrected_profile_distance
from node import Node


def get_nodes_to_possibly_rearrange(neighbor_node_1, neighbor_node_2):
    pass


def nearest_neighbor_interchange(node_a, node_b, node_c, node_d):
    dist_1 = log_corrected_profile_distance(node_a.get_profile(), node_b.get_profile()) + log_corrected_profile_distance(node_c.get_profile(), node_d.get_profile())
    dist_2 = log_corrected_profile_distance(node_a.get_profile(), node_c.get_profile()) + log_corrected_profile_distance(node_b.get_profile(), node_d.get_profile())
    dist_3 = log_corrected_profile_distance(node_b.get_profile(), node_c.get_profile()) + log_corrected_profile_distance(node_a.get_profile(), node_d.get_profile())
    if dist_1 < dist_2 and dist_1 < dist_3:
        return
    if dist_2 < dist_3:
        # change topology to dist2 topology
        return
    else:
        # change topology to dist3 topology
        return
