from distance_calculations import branch_length

def newick_format(node, root_node):
    """
    Formats the tree in Newick format.
    :param node_label: the label of the node to start the formatting from
    :type node_label: str
    :param all_nodes: all nodes
    :type all_nodes: dict(str, Node)
    :return: the tree in Newick format
    :rtype: str
    """
    if not node.get_children():
        return node.get_label() + ":" + str(branch_length(node, node.get_parent(), root_node))
    children = node.get_children()
    output = "(" + newick_format(children[0], root_node) + "," + newick_format(children[1], root_node) + ")"
    if not node.get_parent():
        output += ";"
    else:
        output += node.get_label() + ":" + str(branch_length(node, node.get_parent(), root_node))
    return output

