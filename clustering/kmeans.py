from math import sqrt
import random
from pprint import pprint
__author__ = 'chester'

number_of_iteration = 10

def clustering(vectors):
    costs = []
    clusters = []
    for i in range(len(vectors)):
        curr_cluster = accurate_k_means(vectors, i+1)
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
    cluster_number = 0
    for i in range(len(diff)):
        if diff[i] == minimum:
            cluster_number = i+2
    return {'cluster_number':cluster_number, 'cluster':clusters[cluster_number-1]}


def accurate_k_means(vectors, k):
    curr_cluster = k_means(vectors, k)
    for i in range(number_of_iteration):
        new_cluster = k_means(vectors, k)
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
    while delta_cost != 0:
        if start:
            current_proxies = new_proxies(vectors, current_cluster, k)
        else:
            start = True
        for i in range(len(vectors)):
            current_cluster[i]  = search_nearest(vectors[i], current_proxies)
        new_cost = cost(vectors, current_proxies, current_cluster)
        delta_cost = current_cost - new_cost
        current_cost = new_cost
        #print('-----------------------------------')
        #print('delta : ')
        #print(delta_cost)
        #print('new : ')
        #print(current_cost)
        #print(current_cluster)
    out = {'cost': current_cost, 'cluster' : current_cluster}
    return out

def cost(vectors, proxies, cluster):
    cost = 0
    for i in range(len(vectors)):
        distance = size(subtract(vectors[i]['vector'], proxies[cluster[i]]))
        cost += distance*distance
    return cost

def subtract(a, b):
    out = []
    for i in range(len(b)):
        out.append(a[i]-b[i])
    return out

def benefit(vectors, proxies, cluster):
    benefit = 0
    for i in range(len(vectors)):
        benefit += dist(vectors[i]['vector'], proxies[cluster[i]])
    return benefit

def new_proxies(vectors, cluster, k):
    proxies = []
    zero_vector = []
    for i in range(len(vectors[0]['vector'])):
        zero_vector.append(0)
    count_cluster = []
    for i in range(k):
        proxies.append(zero_vector)
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
    sum_vector = []
    for i in range(len(a)):
        sum_vector.append(a[i]+ b[i]/devide_factor)
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
    for i in vector:
        sum += i*i
    return sqrt(sum)

def dist(a, b):
    dist = 0
    for i in range(len(a)):
        dist += a[i]*b[i]
    return dist

def initial_points(vectors, k):
    random_indexes = []
    init_points = []
    for i in range(1, k+1):
        r = random.randrange(0,len(vectors))
        while (r in random_indexes):
            r = random.randrange(0,len(vectors))
        random_indexes.append(r)
    for r in random_indexes:
        temp = normalize(vectors[r]['vector'])
        init_points.append(temp)
    return init_points

def normalize(vector):
    vector_size = size(vector)
    temp = []
    if vector_size == 0:
        return vector
    for i in range(len(vector)):
        temp.append(vector[i]/vector_size)
    return temp
def main():
    vectors = [{'vector':[2,2,2 ,2], 'id':1},{'vector':[1,1,1 , 3], 'id':2},{'vector':[1,3,3, 3], 'id':3}, {'vector':[1,10,3, 10], 'id':3}, {'vector':[10,1,30, 10], 'id':3}]
    for vec in vectors:
        vec['vector'] = normalize(vec['vector'])
    #print(dist(vectors[0]['vector'],vectors[1]['vector']))
    pprint(clustering(vectors))
if __name__ == '__main__':
    main()
