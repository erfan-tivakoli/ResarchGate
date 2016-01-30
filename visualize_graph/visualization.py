import pickle

__author__ = 'Rfun'
from crawler.Graph import *
import networkx as nx
import matplotlib.pyplot as plt

class visualization():
    def __init__(self, graph):
        self.G = nx.DiGraph()
        self.G.add_nodes_from(list(graph.get_nodes()))
        self.G.add_edges_from(list(graph.get_inner_edges()))

    def draw_graph(self):
        nx.draw(self.G)

def main():
    with open('../graph.pkl', 'rb') as pickled_graph:
        graph = pickle.load(pickled_graph)
    v = visualization(graph)
    v.draw_graph()
    plt.savefig("path.png")

if __name__ == '__main__':
    main()