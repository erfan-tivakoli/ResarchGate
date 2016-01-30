
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
        result = 'nodes:' + '\n'
        result += '\n'.join(node for node in self.nodes)
        result += '\n'
        result += 'edges:' + '\n'
        result += '\n'.join(edge.__str__() for edge in self.edges)

        return result

    def get_inner_edges(self):
        inner_edge = set({})
        for edge in self.edges:
            if (edge[0] in self.nodes and edge[1] in self.nodes):
                inner_edge.add(edge)

        return inner_edge

    def save_to_gexf(self):
        inner_edge = self.get_inner_edges()
        with open('graph.gexf', 'w') as gephi_file:
            gephi_file.write('<?xml version="1.0" encoding="UTF-8"?>' + '\n' + \
                             '<gexf xmlns="http://www.gephi.org/gexf" xmlns:viz="http://www.gephi.org/gexf/viz">' + '\n' + \
                             '<graph type="static">' + '\n' + \
                             '<attributes class="node" type="static">' + '\n' + \
                             '<attribute id="label" title="label" type="string"/>' + '\n' + \
                             '</attributes>' + '\n' + \
                             '<nodes>' + '\n')
            counter = 0
            for node in self.nodes:
                gephi_file.write('<node id="%s" label="%s" >\n' %(node, node))
                gephi_file.write('<viz:color b="72" g="160" r="233"/>\n')
                gephi_file.write('<attvalues/>\n</node>\n')
                counter += 1
            gephi_file.write('</nodes>\n')
            gephi_file.write('<edges>\n')
            counter = 0
            for (source, destination) in inner_edge:
                gephi_file.write('<edge id="%d" source="%s" target="%s"/>\n' %(counter, source, destination))
                counter += 1
            gephi_file.write('</edges>\n</graph>\n</gexf>\n')
