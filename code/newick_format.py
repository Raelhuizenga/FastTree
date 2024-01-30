from distance_calculations import branch_length

def newick_format(node, root_node):
    """
    Formats the tree in Newick format.
    :param node: the node to start from
    :type node: Node
    :param root_node: the root node of the tree
    :type root_node: Node
    :return: the tree in Newick format
    :rtype: str
    """
    if not node.get_children():
        return node.get_label()
    children = node.get_children()
    branch_length_0_p = branch_length(children[0], node, root_node)
    branch_length_1_p = branch_length(children[1], node, root_node)
    # If branch length is negative, set to 0 and add to sister branch length
    if branch_length_0_p < 0:
        branch_length_1_p -= branch_length_0_p
        branch_length_0_p = 0
    if branch_length_1_p < 0:
        branch_length_0_p -= branch_length_1_p
        branch_length_1_p = 0
    output = "(" + newick_format(children[0], root_node) + ":" + str(round(branch_length_0_p, 3)) + "," + newick_format(children[1], root_node) + ":" + str(round(branch_length_1_p, 3)) + ")"
    if not node.get_parent():
        output += ";"
    else:
        output += node.get_label()
    return output

