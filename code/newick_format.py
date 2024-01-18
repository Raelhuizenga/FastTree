from distance_calculations import branch_length

def newick_format(root_node):
    """
    Formats the tree in Newick format.
    :param node_label: the label of the node to start the formatting from
    :type node_label: str
    :param all_nodes: all nodes
    :type all_nodes: dict(str, Node)
    :return: the tree in Newick format
    :rtype: str
    """
    if not root_node.get_children():
        return root_node.get_label() + ":" + str(1)
    children = root_node.get_children()
    output = "(" + newick_format(children[0]) + "," + newick_format(children[1]) + ")"
    if not root_node.get_parent():
        output += ";"
    else:
        output += root_node.get_label() + ":" + str(1)
    return output

