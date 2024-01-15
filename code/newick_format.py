def newick_format(node_label, all_nodes):
    print("node_label: ", node_label)
    node = all_nodes[node_label]
    print("node: ", node)
    print("node.get_children(): ", node.get_children())
    if not node.get_children():
        return node.get_label()
    children = node.get_children()
    output =  "(" + newick_format(children[0].get_label(), all_nodes) + "," + newick_format(children[1].get_label(), all_nodes) + ")"
    # if node.get_parent():
    #     output += ";"
    return output