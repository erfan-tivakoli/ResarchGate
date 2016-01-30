from collections import OrderedDict
import json
import operator
import os
import pickle
from pprint import pprint
from random import random
import elasticsearch

__author__ = 'chester'
from elasticsearch import Elasticsearch

abs_factor = 3
title_factor = 4
author_factor = 1
page_rank_factor = 200

def search(query, number_of_retrieves):
    es = Elasticsearch()
    page_rank = load_page_rank()
    res_abstract = search_by_field(es, query, 'abstract')
    res_title = search_by_field(es, query, 'title')
    res_authors = search_by_field(es, query, 'authors')
    final_result = {}
    add_score(res_abstract, final_result, abs_factor)
    add_score(res_title, final_result, title_factor)
    add_score(res_authors, final_result, author_factor)

    for id in final_result:
        final_result[id]['page_rank'] = page_rank[id]
        final_result[id]['score'] += page_rank[id]*page_rank_factor
    final_result = (sorted(final_result.items(), key=lambda kv: kv[1]['score'], reverse=True))
    bounded_results = []
    for i in range(min([number_of_retrieves,len(final_result)])):
        bounded_results.append(final_result[i])
    return bounded_results

def add_score(curr_result, final_result, priority):
    for doc in curr_result:
        id = doc['_id']
        if id in final_result:
            final_result[id]['score'] += doc['_score']*priority
        else:
            source = doc['_source']
            final_result[id] = {'title':source['title'],'abstract':source['abstract'],'authors':source['authors'],'score':doc['_score']*priority}

def load_page_rank():
    with open('../crawler/page_rank.json','r') as f:
        page_rank = json.loads(f.read())
    #page_rank = {}
    #path = os.path.join(os.path.dirname(__file__).replace('elastic', ''), 'all_jsons')
    #for filename in os.listdir(path):
    #    with open(path + '/' + filename, 'r') as f:
    #        real_doc = json.loads(f.read())
    #        page_rank[real_doc['datas']['publication_uid']] = random()
    return page_rank


def search_by_field(es, query, field):
    ALL_QUERY = {"query": {"match": {field: query}}}
    rs = es.search(
                index='researchgate_index',
                size = 1000,
                body=ALL_QUERY
            )
    return rs['hits']['hits']
def main():
    es = Elasticsearch()
    #pprint(search_by_field(es, 'Reinforcement Learning in Partially', 'abstract'))

if __name__ == '__main__':
    main()