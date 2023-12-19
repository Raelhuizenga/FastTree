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
