def FastTree(Sequences):
    sequenceList = list(Sequences.values())
    n = len(sequenceList)
    l = len(sequenceList[0])
    A,C,T,G = FormProfile(sequenceList)
    topHits = TopHits(Sequences)
    

def FormProfile(Sequences): # Should be O(nla), a = 4 (alphabet size)
    
    n = len(Sequences)
    l = len(Sequences[0])

    A=[]
    C=[]
    G=[]
    T=[]
    for i in range(l):
        A.append(0.0)
        C.append(0.0)
        G.append(0.0)
        T.append(0.0)
        for j in range(n):
            if len(Sequences[j]) != l:
                 raise ValueError(str(j) + 'th sequence of '+ str(n) + ' sequences is not of the same length')
            if Sequences[j][i] == "A":
                A[i] += 1/n
            elif Sequences[j][i] == "G":
                G[i] += 1/n
            elif Sequences[j][i] == "C":
                C[i] += 1/n
            elif Sequences[j][i] == "T":
                T[i] += 1/n
    return A, C, G, T

def TopHits(Sequences):
    m = int(n**(1/2))
    topHits = {}
    return topHits

def BestHits(Sequences):
    bestHits = {}
    return bestHits


if __name__ == '__main__':
    data = open('../data/test-small.txt', 'r').read().split(">")
    sequences = {}
    for seq in data[1::]:
        label, DNA = seq.splitlines()
        sequences[label] = DNA
    
    
#formProfile(sequences)






