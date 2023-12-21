class Node:
    """ 
    A class used to represent a node in the tree
    :param age: the number of merges of nodes that have occurred to obtain the node
    :type age: int
    :param profile: the total profile of the sequences in the node
    :type profile: list[list[float]]
    :param top_hits: the top hits of the node
    :type top_hits: list[Node]
    :param up_distance: the up distance of the node, defined 0 for leaf nodes
    :type up_distance: float
    :param label: the label of the node, defined in the input file for leaf nodes,
        and assigned by the algorithm for internal nodes
    :type label: str
    :param children: the children of the node
    :type children: list[Node]
    """

    def __init__(self, age, profile, top_hits, up_distance, label, children):
        """
        Constructs all the necessary attributes for the node object
        :param age: the number of merges of nodes that have occurred to obtain the node
        :type age: int
        :param profile: the total profile of the sequences in the node
        :type profile: list[list[float]]]
        :param top_hits: the top hits of the node
        :type top_hits: dict[Node] = neighbor joining criterion value
        :param up_distance: the up distance of the node, defined 0 for leaf nodes
        :type up_distance: float
        :param label: the label of the node, defined in the input file for leaf
            nodes, and assigned by the algorithm for internal nodes
        :type label: str
        :param children: the children of the node
        :type children: list[Node]
        """        
        self.label = label
        self.age = age
        self.profile = profile
        self.top_hits = top_hits
        self.up_distance = up_distance
        self.children = children

    def get_label(self):
        return self.label
    
    def get_age(self):
        return self.age
    
    def get_profile(self):
        return self.profile
    
    def get_top_hits(self):
        return self.top_hits
    
    def get_up_distance(self):
        return self.up_distance

    def get_children(self):
        return self.children
    
    def set_label(self, label):
        self.label = label

    def set_age(self, age):
        self.age = age

    def set_profile(self, profile):
        self.profile = profile
    
    def set_up_distance(self, up_distance):
        self.up_distance = up_distance
    
    def set_top_hits(self, top_hits):
        self.top_hits = top_hits

    def set_children(self, children):
        self.children = children

    def __eq__(self, other):
        if self.label == other.get_label():
            return True
        return False

