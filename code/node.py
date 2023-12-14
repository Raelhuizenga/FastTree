class Node:
    def __init__(self, age, profile, top_hits, up_distance, label, children):
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

