class Node:

    def __init__(self, age, profile, top_hits, up_distance, label, children, active, parent, variance_correction, lambda_val):
        """
        Constructs all the necessary attributes for the node object
        :param age: the number of merges of nodes that have occurred to obtain the node
        :type age: int
        :param profile: the total profile of the sequences in the node
        :type profile: list[list[float]]]
        :param top_hits: the labels of top hits of the node with their distance to the node 
        :type top_hits: dict(str, float)
        :param up_distance: the up distance of the node, defined 0 for leaf nodes
        :type up_distance: float
        :param label: the label of the node, defined in the input file for leaf
            nodes, and the joined labels of the children for internal nodes
        :type label: str
        :param children: the children of the node
        :type children: list[Node]
        :param active: if the node is active
        :type active: boolean
        :param parents: the parent of the node
        :type parents: Node
        :param variance_correction: the variance correction of the node
        :type variance_correction: float
        :param lambda_val: the lambda value of the node
        :type lambda_val: float
        """        
        self.label = label
        self.age = age
        self.profile = profile
        self.top_hits = top_hits
        self.up_distance = up_distance
        self.children = children
        self.active = active
        self.parent = parent
        self.variance_correction = variance_correction
        self.lambda_val = lambda_val

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

    def get_active(self):
        return self.active

    def get_parent(self):
        return self.parent

    def get_variance_correction(self):
        return self.variance_correction

    def get_lambda(self):
        return self.lambda_val
    
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

    def set_active(self, active):
        self.active = active

    def set_parent(self, parent):
        self.parent = parent

    def set_variance_correction(self, variance_correction):
        self.variance_correction = variance_correction

    def set_lambda(self, lambda_val):
        self.lambda_val = lambda_val

    def __eq__(self, other):
        if self.label == other.get_label():
            return True
        return False

