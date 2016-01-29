import operator

__author__ = 'Rfun'
from crawler.Graph import *
import numpy as np
from numpy import linalg as la
import pickle
import json


class PageRank():
    def __init__(self, graph):
        self.graph = graph
        self.nodes = list(self.graph.get_nodes())
        self.inner_edges = self.graph.get_inner_edges()
        self.nodes_size = len(self.nodes)
        self.transaction_matrix = np.zeros((self.nodes_size, self.nodes_size), dtype=np.int)
        self.teleport = 0.1


    def calc_transition_matrix(self):
        for edge in self.inner_edges:
            self.transaction_matrix[self.nodes.index(edge[0])][self.nodes.index(edge[1])] = 1

        for i in range(self.nodes_size):
            row_sum = sum(self.transaction_matrix[i])
            if row_sum < 1:
                for j in range(self.nodes_size):
                    self.transaction_matrix[i][j] = 1 / (self.nodes_size)
            else:
                for j in range(self.nodes_size):
                    self.transaction_matrix[i][j] = 1 / (row_sum)

        self.transaction_matrix = self.transaction_matrix * (1 - self.teleport) + \
                                  np.ones((self.nodes_size, self.nodes_size)) * (1 / self.nodes_size) * (self.teleport)
        self.transaction_matrix = self.transaction_matrix.transpose()

    def calc_page_rank(self):
        va, ve = la.eig(self.transaction_matrix)
        for i in range(len(va)):
            if la.norm(va[i] - 1) < 0.001:
                break

        ve_real = []
        for j in range(self.nodes_size):
            ve_real.append(la.norm(ve[j, i]))
        ve_real = ve_real/sum(ve_real)
        return ve_real


def run():
    with open('../graph.pkl', 'rb') as pickled_graph:
        graph = pickle.load(pickled_graph)
    pr = PageRank(graph)
    pr.calc_transition_matrix()
    page_rank_vector = pr.calc_page_rank()
    page_rank_dict = {}
    for i in range(len(pr.nodes)):
        page_rank_dict[pr.nodes[i]] = la.norm(page_rank_vector[i])

    with open('page_rank.json', 'w') as json_file:
        json.dump(page_rank_dict, json_file)


if __name__ == '__main__':
    run()
