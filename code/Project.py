import numpy as np


def fast_tree(sequences):
    sequence_list = list(sequences.values())
    n = len(sequence_list)
    l = len(sequence_list[0])
    A, C, T, G = form_profile(sequence_list)
    top = top_hits(sequence_list, n)


def form_profile(sequences):  # Should be O(nla), a = 4 (alphabet size)

    n = len(sequences)
    l = len(sequences[0])

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
            if len(sequences[j]) != l:
                raise ValueError(str(j) + 'th sequence of ' + str(n) + ' sequences is not of the same length')
            if sequences[j][i] == "A":
                A[i] += 1 / n
            elif sequences[j][i] == "G":
                G[i] += 1 / n
            elif sequences[j][i] == "C":
                C[i] += 1 / n
            elif sequences[j][i] == "T":
                T[i] += 1 / n
    return A, C, G, T


def neighbor_joining_criterion(pattern_1, pattern_2, sequences):
    return hamming_distance(pattern_1, pattern_2) - average_out_distance(pattern_1, sequences) - average_out_distance(
        pattern_2, sequences)


def hamming_distance(pattern_1, pattern_2):
    distance = 0
    for i in range(len(pattern_1)):
        if pattern_1[i] != pattern_2[i]:
            distance += 1
    return distance


def up_distance(pattern):
    # zero if leaf node
    # else depth
    pass


def average_out_distance(pattern, active_nodes):
    dist = 0
    for i in range(len(active_nodes)):
        dist += hamming_distance(pattern, active_nodes[i])
    return dist / (len(active_nodes) - 2)


def top_hits(seed_sequences, n):
    top_hits_dict = {}
    m = int(np.sqrt(n))
    while len(seed_sequences) > m:
        print(f'm = {m}')
        print(f'seedsequences = {len(seed_sequences)}')
        single_seed_sequence = seed_sequences[np.random.randint(0, len(seed_sequences))]
        close_neighbors = calculate_close_neighbors(single_seed_sequence, seed_sequences, m)
        top_hits_helper = calculate_close_neighbors(single_seed_sequence, seed_sequences, 2 * m)
        for neighbor in close_neighbors:
            top_hits_dict[neighbor] = calculate_close_neighbors(neighbor, top_hits_helper, m)
            seed_sequences.remove(neighbor)
    for remaining_sequence in seed_sequences:
        top_hits_sequences = seed_sequences.copy()
        top_hits_dict[remaining_sequence] = top_hits_sequences.remove(remaining_sequence)
    return top_hits_dict


def calculate_close_neighbors(seed, sequences, m):
    if len(sequences) < m:
        m = len(sequences)
    hamming_distances = []
    for i in range(len(sequences)):
        hamming_distances.append(neighbor_joining_criterion(seed, sequences[i], sequences))
    sorted_hamming_distances = hamming_distances.copy()
    sorted_hamming_distances.sort()
    m_distance = sorted_hamming_distances[m - 1]
    return [sequences[i] for i in range(len(sequences)) if hamming_distances[i] > m_distance]


def best_hits(sequences):
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
