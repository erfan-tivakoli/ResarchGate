__author__ = 'Rfun'

class Graph():

    def __init__(self):
        self.nodes = set({})
        self.edges = set({})

    def add_node(self, node_id):
        self.nodes.add(node_id)

    def add_edge(self, source, destination):
        self.edges.add((source, destination))

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges

    def __str__(self):
        result = 'node set is: '
        for node in self.nodes:
            result += node + '\n'

        for edge in self.edges:
            result += edge + '\n'

        return result
