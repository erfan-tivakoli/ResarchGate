import json
from math import sqrt
import pickle
import random
from pprint import pprint
__author__ = 'chester'

number_of_iteration = 20

def clustering(vectors):
    costs = []
    clusters = []
    for i in range(60):
        curr_cluster = accurate_k_means(vectors, i+1)
        print('one cluster iteration ' + str(i))
        print('-----------------------------')
        costs.append(curr_cluster['cost'])
        clusters.append(curr_cluster)
    print(costs)
    diff = []
    index = len(costs)-1
    for i in range(1,len(costs)):
        if costs[i] > costs[i-1]:
            index = i
            print(costs[i])
            print(costs[i-1])
            break
    print(index)
    for i in range(1,index):
        diff.append((costs[i+1]-2*costs[i]+costs[i-1]))
    print(diff)
    minimum = min(diff,)
    cluster_number = 1
    for i in range(len(diff)):
        if diff[i] == minimum:
            cluster_number = i+2
    return {'cluster_number':cluster_number, 'cluster_1':clusters[cluster_number-1], 'cluster_2':clusters[cluster_number-2]}


def accurate_k_means(vectors, k):
    curr_cluster = k_means(vectors, k)
    for i in range(number_of_iteration):
        new_cluster = k_means(vectors, k)
        print('intra cluster iteration : ' + str(i))
        if new_cluster['cost'] < curr_cluster['cost']:
            curr_cluster = new_cluster
    return curr_cluster

def k_means(vectors, k):
    current_proxies = initial_points(vectors, k)
    current_cost = 100
    delta_cost = 1
    start = False
    current_cluster = []
    for i in range(len(vectors)):
        current_cluster.append(0)
    while delta_cost > 0.001:
        if start:
            current_proxies = new_proxies(vectors, current_cluster, k)
        else:
            start = True
        for i in range(len(vectors)):
            current_cluster[i]  = search_nearest(vectors[i], current_proxies)
        new_cost = cost(vectors, current_proxies, current_cluster)
        delta_cost = current_cost - new_cost
        current_cost = new_cost
    out = {'cost': current_cost, 'cluster' : current_cluster}
    return out

def cost(vectors, proxies, cluster):
    cost = 0
    for i in range(len(vectors)):
        distance = size(subtract(vectors[i]['vector'], proxies[cluster[i]]))
        cost += distance*distance
    return cost

def subtract(a, b):
    return sum_vector(a, b, -1)

def benefit(vectors, proxies, cluster):
    benefit = 0
    for i in range(len(vectors)):
        benefit += dist(vectors[i]['vector'], proxies[cluster[i]])
    return benefit

def new_proxies(vectors, cluster, k):
    proxies = []
    count_cluster = []
    for i in range(k):
        proxies.append({})
        count_cluster.append(0)
    for i in range(len(cluster)):
        count_cluster[cluster[i]] += 1
    for i in range(len(cluster)):
        devide_factor = count_cluster[cluster[i]]
        proxies[cluster[i]] = sum_vector(proxies[cluster[i]], vectors[i]['vector'], devide_factor)
    for i in range(k):
        proxies[i] = normalize(proxies[i])
    return proxies

def sum_vector(a, b, devide_factor):
    sum_vector = { k: a.get(k, 0) + b.get(k, 0)/devide_factor for k in set(a) | set(b) }
    #for i in range(len(a)):
    #    sum_vector.append(a[i]+ b[i]/devide_factor)
    return sum_vector
def search_nearest(doc, current_proxies):
    maximum = -1
    index = 0
    for i in range(len(current_proxies)):
        distance = dist(current_proxies[i], doc['vector'])
        if  distance > maximum:
            index = i
            maximum = distance
    return index

def size(vector):
    sum = 0
    for term in vector:
        sum += vector[term]*vector[term]
    return sqrt(sum)

def dist(a, b):
    dist = 0
    for term in set(a) & set(b):
        dist += a[term]*b[term]
    return dist

def initial_points(vectors, k):
    random_indexes = []
    init_points = []
    all_indexes = []
    for i in range(len(vectors)):
        all_indexes.append(i)
    for i in range(k):
        r = random.randrange(0,len(all_indexes))
        random_indexes.append(all_indexes[r])
        all_indexes.remove(all_indexes[r])
    for r in random_indexes:
        temp = normalize(vectors[r]['vector'])
        init_points.append(temp)
    return init_points

def normalize(vector):
    vector_size = size(vector)
    if vector_size == 0:
        return vector
    for term in vector:
        vector[term] /= vector_size
    return vector
def load_vectors():
    with open('../vectors.txt', 'rb') as f:
        return pickle.load(f)
def normalize_collection(vectors):
    for vec in vectors:
        vec['vector'] = normalize(vec['vector'])
def main():
    #vectors = [{'vector':{'salam':2,'khiar':2, 'havij':1},'id':0},{'vector':{'salam':2,'saeed':1},'id':1},{'vector':{'hamid':2,'saeed':1,'salam':1},'id':2},{'vector':{'havij':2,'ali':0.5,'salam':1},'id':3},{'vector':{'khiar':1,'ali':5,'salam':1},'id':4}]
    vectors = load_vectors()[0]
    normalize_collection(vectors)
    result = clustering(vectors)
    pprint(result)
    with open('clustering.json', 'w') as json_file:
            json.dump(result, json_file)

if __name__ == '__main__':
    main()
