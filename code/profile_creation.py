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
