def form_profile(sequences):  # Should be O(nla), a = 4 (alphabet size)
    """
    Forms a profile from the given sequences.
    :param sequences: the sequences to form a profile from
    :type sequences: list[str]
    :return: the profile
    :rtype: list[list[float]]
    """
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
    return [A, C, G, T]


def create_combined_profile(node_1, node_2):
    profile_1 = node_1.get_profile()
    profile_2 = node_2.get_profile()
    print(len(profile_1), len(profile_1[0]))
    print(len(profile_2), len(profile_2[0]))
    new_profile = []
    for i in range(len(profile_1)):
        row = []
        for j in range(len(profile_1[0])):
            row.append(profile_1[i][j] + profile_2[i][j] / 2)
        new_profile.append(row)
    return new_profile
