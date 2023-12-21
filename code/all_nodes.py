class AllNodes:
    def __init__(self, nodes):
        self.nodes = nodes

    def get_by_label(self, label):
        for node in self.nodes:
            if node.get_label() == label:
                return node

    def add_node(self, node):
        self.nodes.append(node)
