import random
from distance_calculations import log_corrected_profile_distance

def newick_format(node_label, all_nodes):
    """
    Formats the tree in Newick format.
    :param node_label: the label of the node to start the formatting from
    :type node_label: str
    :param all_nodes: all nodes
    :type all_nodes: dict(str, Node)
    :return: the tree in Newick format
    :rtype: str
    """
    node = all_nodes[node_label]
    if not node.get_children():
        return node.get_label() + ":" + str(branch_length(node, node.get_parent(), all_nodes))
    children = node.get_children()
    output = "(" + newick_format(children[0].get_label(), all_nodes)+ "," + newick_format(children[1].get_label(), all_nodes) + ")"
    if not node.get_parent():
        output += ";"
    else:
        output += node.get_label() + ":" + str(branch_length(node, node.get_parent(), all_nodes))
    return output

def branch_length(node_1, node_2, all_nodes):
    # node_1 = all_nodes[node_1]
    # node_2 = all_nodes[node_2]
    if node_1.get_children() and node_2.get_children():
        A = node_1.get_children()[0].get_label()
        B = node_1.get_children()[1].get_label()
        C = node_2.get_children()[0].get_label()
        D = node_2.get_children()[1].get_label()
        return (log_corrected_profile_distance(A,C,all_nodes) + log_corrected_profile_distance(A,D,all_nodes) + \
                log_corrected_profile_distance(B,C,all_nodes) + log_corrected_profile_distance(B, D, all_nodes))/4 \
                - (log_corrected_profile_distance(A, B, all_nodes) + log_corrected_profile_distance(C, D, all_nodes))/2
    elif node_1.get_children() and not node_2.get_children():
        A = node_1.get_children()[0].get_label()
        B = node_1.get_children()[1].get_label()
        C = node_2.get_label()
        return (log_corrected_profile_distance(C, A, all_nodes)+log_corrected_profile_distance(C, B, all_nodes) - \
                log_corrected_profile_distance(A, B, all_nodes)) / 2
    elif not node_1.get_children() and node_2.get_children:
        A = node_1.get_label()
        B = node_2.get_children()[0].get_label()
        C = node_2.get_children()[1].get_label()
        return (log_corrected_profile_distance(A, B, all_nodes)+log_corrected_profile_distance(A, C, all_nodes) - \
                log_corrected_profile_distance(B, C, all_nodes)) / 2
    else:
        A = node_1.get_label()
        B = node_2.get_label()
        return log_corrected_profile_distance(A, B, all_nodes)