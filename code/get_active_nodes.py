def get_active_nodes(all_nodes):
    active_nodes = all_nodes.copy()
    for key, value in all_nodes.items():
        if not value.get_active():
            del active_nodes[key]
    return active_nodes
