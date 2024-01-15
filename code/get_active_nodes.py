def get_active_nodes(all_nodes):
    active_nodes = all_nodes.copy()
    for key, value in all_nodes.items():
        if not value.get_active():
            del active_nodes[key]
    return active_nodes


def give_active_node(node_label, all_nodes):
    node = all_nodes[node_label]
    while not node.get_active():
        node = node.get_parent()
    return node.get_label()
