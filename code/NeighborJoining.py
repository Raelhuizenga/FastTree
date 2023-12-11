import numpy as np

def NeighborJoining(D,n,labels):
    if n == 2:
        T = {(labels[0],labels[1]): D[0][1], (labels[1],labels[0]): D[0][1]}
        return T
    D_nj, i, j = ConstructNeighborJoiningMatrix(D,n)
    i_label = labels[i]
    j_label = labels[j]
    m_label = max(labels) +1
    labels = np.append(labels,max(labels)+1)
    Delta = (sum(D[i,:]) - sum(D[j,:]))/(n-2)
    limbLengthi = (1/2)*(D[i][j] + Delta)
    limbLengthj = (1/2)*(D[i][j] - Delta)
    
    Dkm = []
    for k in range(n):
        Dkm.append((1/2)*(D[k][i]+D[k][j]-D[i][j]))
    D = np.insert(D,len(D),Dkm,axis=1)
    Dkm.append(0)
    D = np.insert(D,len(D),Dkm,axis=0) 
    D = np.delete(D,j,1)
    D = np.delete(D,j,0)
    labels = np.delete(labels,j)
    D = np.delete(D,i,1)
    D = np.delete(D,i,0)
    labels = np.delete(labels,i)
    
    
    T = NeighborJoining(D, n - 1,labels)
    
    T[(i_label,m_label)] = limbLengthi 
    T[(j_label,m_label)] = limbLengthj 
    T[(m_label,i_label)] = limbLengthi 
    T[(m_label,j_label)] = limbLengthj
    return dict(sorted(T.items()))

def ConstructNeighborJoiningMatrix(D,n):
    D_nj = np.zeros((n,n))
    min_v = 0
    for i in range(n-1):
        Dist_i = sum(D[i,:])
        for j in range(i+1,n):
            Dist_j = sum(D[j,:])
            Dij = (n-2)*D[i][j] - Dist_i - Dist_j
            D_nj[i][j] = Dij
            D_nj[j][i] = Dij
            if Dij < min_v:
                min_v = Dij
                min_i = i
                min_j = j
    return D_nj, min_i, min_j

n = int(open('data.txt', 'r').read().splitlines()[0])
paths = open('data.txt', 'r').read().splitlines()[1::]
D = np.zeros((n,n))
for i,leaf in enumerate(paths):
    D[i] = ' '.join(leaf.split(" ")).split()

labels = np.linspace(0,n-1,n).astype(int)
result = NeighborJoining(D, n, labels)
for nodes,w in result.items():
    print(str(nodes[0])+"->"+str(nodes[1])+":"+'%.3f'%(w))






