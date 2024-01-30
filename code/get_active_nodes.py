def get_active_nodes(all_nodes):
    """
    Returns a dictionary with all active nodes.
    :param all_nodes: all nodes with their labels
    :type all_nodes: dict(label, node)
    :return: dictionary with all active nodes
    :rtype: dict(label, node)
    """
    active_nodes = all_nodes.copy()
    for key, value in all_nodes.items():
        if not value.get_active():
            del active_nodes[key]
    return active_nodes


def give_active_node(node_label, all_nodes):
    """
    Returns the closest active node in the lineage of the node with the given label.
    :param node_label: the label of the node
    :type node_label: str
    :param all_nodes: all nodes with their labels
    :type all_nodes: dict(label, node)
    :return: the closest active node
    :rtype: Node
    """
    if node_label not in all_nodes:
        raise ValueError("label not found in node list")
    node = all_nodes[node_label]
    while not node.get_active():
        node = node.get_parent()
    return node.get_label()
