__author__ = 'Rfun'
import json
from crawler.Graph import *
from crawler.utils import *
import pickle


class ItemPipeline():
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.all_items = []
        self.all_authors = []
        self.graph = Graph()

    def add_items(self, all_datas):
        # print('started to add items')
        self.dump_json(all_datas)
        self.scheduler.add(all_datas['cited_in'][:10] + all_datas['references'][:10])
        self.add_to_graph(publication_uid=all_datas['datas']['publication_uid'], cited_in=all_datas['cited_in'],
                          references=all_datas['references'])
        # print('finished adding')

    def add_authors(self, all_authors):

        json_format = {}
        json_format['author_name'] = all_authors['author_name']
        (all_authors.__delitem__('author_name'))
        json_format['publications'] = all_authors
        print('dumping')
        print(json_format)
        self.dump_author(json_format)
        print('dumped')
        for value in all_authors.values():
            self.scheduler.add(value)


    def dump_author(self,result):
        with open('../authors/'+ result['author_name']+'.json', 'w') as json_file:
            json.dump(result, json_file)
        self.all_authors += [result]

    def dump_json(self, result):
        publication_uid = result['datas']['publication_uid']
        with open('all_jsons/' + str(publication_uid) + '.json', 'w') as json_file:
            json.dump(result, json_file)
        self.all_items += [result]

    def get_items_len(self):
        return len(self.all_items)

    def add_to_graph(self, publication_uid, cited_in, references):
        self.graph.add_node(publication_uid)
        for link in cited_in:
            self.graph.add_edge(get_uid_from_url(link), publication_uid)
        for link in references:
            self.graph.add_edge(publication_uid, get_uid_from_url(link))

    def get_graph(self):
        return self.graph

    def pickle_graph(self):
        with open('graph.pkl', 'wb') as pickled_graph:
            pickle.dump(self.graph, pickled_graph)

    def save_to_text_file(self):
        with open('graph.txt', 'w') as text_graph:
            text_graph.write(self.graph.__str__())