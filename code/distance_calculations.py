def neighbor_joining_criterion(node_i, node_j, nodes):
    return profile_distance(node_i.get_profile(), node_j.get_profile()) - node_i.get_up_distance() \
        - node_j.get_up_distance() + average_out_distance(node_i, nodes) - average_out_distance(node_j, nodes)


def hamming_distance(pattern_1, pattern_2):
    distance = 0
    for i in range(len(pattern_1)):
        if pattern_1[i] != pattern_2[i]:
            distance += 1
    return distance


# preprint paper page 11
def up_distance(profile_i, profile_j):
    return profile_distance(profile_i, profile_j) / 2


# preprint paper page 3
def profile_distance(profile_i, profile_j):
    profile_distance_value = 0
    for l in range(len(profile_i[0])):
        for a in range(4):
            for b in range(4):
                if a != b:
                    profile_distance_value += profile_i[a][l] * profile_j[b][l]
    profile_distance_value = profile_distance_value / len(profile_i[0])
    return profile_distance_value


def average_out_distance(node, active_nodes):
    dist = 0
    for i in range(len(active_nodes)):
        dist += profile_distance(node.get_profile(), active_nodes[i].get_profile()) - node.get_up_distance() \
                - active_nodes[i].get_up_distance()
    return dist / (len(active_nodes) - 2)