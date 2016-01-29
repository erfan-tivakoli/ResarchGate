import json
from math import log2
import pickle
import operator

__author__ = 'chester'

def cluster_labeling():
    index = load_vectors()
    vectors = index[0]
    vocab = index[1]
    cluster_info = load_cluster()
    cluster = cluster_info['cluster_2']['cluster']
    cluster_num = cluster_info['cluster_number']-1
    N_11 = initiate_Nij(cluster_num, vocab)
    N_10 = initiate_Nij(cluster_num, vocab)
    N_01 = initiate_Nij(cluster_num, vocab)
    N_00 = initiate_Nij(cluster_num, vocab)
    print(len(cluster))
    for i in range(len(vectors)):
        vec = vectors[i]['vector']
        cl = cluster[i]
        for term in vocab:
            if term in vec:
                N_11[cl][term] += 1
                for i in range(cluster_num):
                    if i != cl:
                        N_10[i][term] += 1
            else:
                N_01[cl][term] += 1
                for i in range(cluster_num):
                    if i != cl:
                        N_00[i][term] += 1
    N__1 = initiate_Nij(cluster_num, vocab)
    N__0 = initiate_Nij(cluster_num, vocab)
    N_0_ = initiate_Nij(cluster_num, vocab)
    N_1_ = initiate_Nij(cluster_num, vocab)
    for i in range(cluster_num):
        for term in vocab:
            N__1[i][term] = N_01[i][term] + N_11[i][term]
            N_1_[i][term] = N_10[i][term] + N_11[i][term]
            N__0[i][term] = N_10[i][term] + N_00[i][term]
            N_0_[i][term] = N_01[i][term] + N_00[i][term]
    MI = dict()
    for i in range(cluster_num):
        MI[i] = dict()
        for term in vocab:
            n01 = not_zero(N_01[i][term])
            n11 = not_zero(N_11[i][term])
            n00 = not_zero(N_00[i][term])
            n10 = not_zero(N_10[i][term])
            n1_ = N_1_[i][term]
            n_1 = N__1[i][term]
            n0_ = N_0_[i][term]
            n_0 = N__0[i][term]
            n = n1_ + n0_
            #print(n)
            #print(n01)
            #print(n10)
            #print(n00)
            #print(n11)
            #print(term)
            #print(vocab[term])
            #print(i)
            #print('-------------------')
            mi = 0
            mi += (n11/n)*log2(n*n11/(n1_*n_1))
            mi += (n01/n)*log2(n*n01/(n0_*n_1))
            mi += (n10/n)*log2(n*n10/(n1_*n_0))
            mi += (n00/n)*log2(n*n00/(n0_*n_0))
            MI[i][term] = mi
    labels = []
    for i in range(len(MI)):
        labels.append(get_maximums(MI[i], 10))
    return labels
def get_maximums(mi, k):
    out = []
    sorted_mi = sorted(mi.items(), key=operator.itemgetter(1))
    for i in range(k):
        out.append(sorted_mi[i][0])
    return out
def not_zero(a):
    if a == 0:
        a += 1
    return a

def initiate_Nij(cluster_num, vocab):
    n = dict()
    for i in range(cluster_num):
        n[i] = dict()
        for term in vocab:
            n[i][term] = 0
    return n
def load_cluster():
    with open('clustering.json', 'r') as f:
        return json.load(f)

def load_vectors():
    with open('../vectors.txt', 'rb') as f:
        return pickle.load(f)

def main():
    print(cluster_labeling())
if __name__ == '__main__':
    main()