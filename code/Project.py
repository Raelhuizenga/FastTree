import numpy as np
from node import Node

def fast_tree(nodes):
    sequence_list = list(nodes.values())
    n = len(sequence_list)
    L = len(sequence_list[0])
    total_profile = form_profile(sequence_list)
    total_up_distance = 0
    total_nodes = []
    for label, seq in nodes.items():
        total_nodes.append(Node(0, form_profile([seq]), [], 0, label))
    top_hits(total_nodes, n)


def form_profile(nodes):  # Should be O(nla), a = 4 (alphabet size)
    n = len(nodes)
    l = len(nodes[0])
    A = []
    C = []
    G = []
    T = []
    for i in range(l):
        A.append(0.0)
        C.append(0.0)
        G.append(0.0)
        T.append(0.0)
        for j in range(n):
            if len(nodes[j]) != l:
                raise ValueError(str(j) + 'th sequence of ' + str(n) + ' nodes is not of the same length')
            if nodes[j][i] == "A":
                A[i] += 1 / n
            elif nodes[j][i] == "G":
                G[i] += 1 / n
            elif nodes[j][i] == "C":
                C[i] += 1 / n
            elif nodes[j][i] == "T":
                T[i] += 1 / n
    return [A, C, G, T]

# paper page 1643
def neighbor_joining_criterion(node_i, node_j, nodes):
    return profile_distance(node_i.get_profile(), node_j.get_profile()) - node_i.get_up_distance()  \
        - node_j.get_up_distance() + average_out_distance(node_i, nodes) - average_out_distance(node_j, nodes)


def hamming_distance(pattern_1, pattern_2):
    distance = 0
    for i in range(len(pattern_1)):
        if pattern_1[i] != pattern_2[i]:
            distance += 1
    return distance

# preprint paper page 11
def up_distance(profile_i,profile_j,L):
    return profile_distance(profile_i, profile_j,L)/2
    

# preprint paper page 3
def profile_distance(profile_i, profile_j,L):
    profile_distance_value = 0
    for l in range(L):
        for a in range(4):
            for b in range(4):
                if a!=b:
                    profile_distance += profile_i[a][l]*profile_j[b][l]
    profile_distance_value = profile_distance_value/L     
    return profile_distance_value


def average_out_distance(node, active_nodes):
    dist = 0
    for i in range(len(active_nodes)):
        dist += profile_distance(node.get_profile(), active_nodes[i].get_profile()) - node.get_up_distance() \
            - active_nodes[i].get_up_distance()
    return dist / (len(active_nodes) - 2)


def top_hits(seed_nodes, n):
    top_hits_dict = {}
    m = int(np.sqrt(n))
    while len(seed_nodes) > m:
        print(f'm = {m}')
        print(f'seedsequences = {len(seed_nodes)}')
        single_seed_node = seed_nodes[np.random.randint(0, len(seed_nodes))]
        close_neighbors = calculate_close_neighbors(single_seed_node, seed_nodes, m)
        # It was unclear from the paper whether the top hits from the seed sequence should be 
        # directly saved and the seed sequence should be removed from seed_nodes
        top_hits_dict[single_seed_node] = close_neighbors
        seed_nodes.remove(single_seed_node)
        top_hits_helper = calculate_close_neighbors(single_seed_node, seed_nodes, 2 * m)
        for neighbor in close_neighbors:
            top_hits_dict[neighbor] = calculate_close_neighbors(neighbor, top_hits_helper, m)
            seed_nodes.remove(neighbor)
    for remaining_sequence in seed_nodes:
        top_hits_sequences = seed_nodes.copy()
        top_hits_dict[remaining_sequence] = top_hits_sequences.remove(remaining_sequence)
    return top_hits_dict


def calculate_close_neighbors(seed, nodes, m):
    if len(nodes) < m:
        m = len(nodes)
    distances = []
    for i in range(len(nodes)):
        distances.append(neighbor_joining_criterion(seed, nodes[i], nodes))
    sorted_distances = distances.copy()
    sorted_distances.sort()
    m_distance = sorted_distances[m - 1]
    return [nodes[i] for i in range(len(nodes)) if distances[i] > m_distance]


def best_hits(nodes):
    best_hits = {}
    return best_hits


if __name__ == '__main__':
    data = open('../data/test-small.txt', 'r').read().split(">")
    sequence_dictionary = {}
    for seq in data[1::]:
        label, DNA = seq.splitlines()
        sequence_dictionary[label] = DNA
    n = top_hits(list(sequence_dictionary.values()), len(sequence_dictionary))
    print(n)
