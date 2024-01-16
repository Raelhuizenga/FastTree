class AllNodes:
    def __init__(self, nodes):
        self.nodes = nodes

    def get_by_label(self, label):
        for node in self.nodes:
            if node.get_label() == label:
                return node

    def add_node(self, node):
        self.nodes.append(node)

def hamming_distance(pattern_1, pattern_2):
    """
    Calculates the hamming distance between two patterns.
    :param pattern_1: the first pattern
    :type pattern_1: str
    :param pattern_2: the second pattern
    :type pattern_2: str
    :return: the hamming distance between pattern_1 and pattern_2
    :rtype: int
    """
    distance = 0
    for i in range(len(pattern_1)):
        if pattern_1[i] != pattern_2[i]:
            distance += 1
    return distance

def calculate_close_neighbors(seed, nodes, m, total_nodes):
    # We also had top_hits_helper which was the same function
    """
    Calculates the m closest neighbors of seed in nodes.
    :param seed: a node
    :type seed: Node
    :param nodes: the nodes to search in
    :type nodes: dict(str, Node)
    :param m: the number of neighbors to return
    :type m: int
    :return: the labels of the m closest neighbors of seed in nodes and their distance
    :rtype: dict(str, float)
    """
    if len(nodes) < m:
        m = len(nodes)
    distances = []
    for label, distance in nodes.items():
        distances.append(neighbor_joining_criterion(seed, total_nodes[label], total_nodes))
    sorted_distances = distances.copy()
    sorted_distances.sort()
    m_distance = sorted_distances[m - 1]
    close_neighbors = {}
    for i, label in enumerate(list(nodes.keys())):
        if distances[i] <= m_distance:
            close_neighbors[label] = distances[i]
    return close_neighbors
