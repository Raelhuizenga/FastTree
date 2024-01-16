from distance_calculations import branch_length

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

