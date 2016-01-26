__author__ = 'chester'
from elasticsearch import Elasticsearch

def index(doc_dict):
    es = Elasticsearch()
    id = doc_dict.pop('key', None)
    es.index(index = 'researchGate_index', doc_type='paper', id = id,body = doc_dict)
