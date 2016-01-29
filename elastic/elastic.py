import json
from math import log
import pickle
from crawler.parser import parse_html
import os

__author__ = 'chester'
from elasticsearch import Elasticsearch
from pprint import pprint

doc_vectors = dict()
es = Elasticsearch()
tf_idf_vectors = []
title_priority = 3

def index():
    docs_list = load_docs()
    es.indices.delete(index='researchgate_index', ignore=[400, 404])
    es.indices.create(index='researchgate_index'
                                            #body =  {"settings": {
                                            #            "analysis": {
                                            #              "analyzer": {
                                            #                "my_analyzer": {
                                            #                  "type": "standard",
                                            #                  "stopwords": [ "title", "of" ]
                                            #                }
                                            #              }
                                            #            }
                                            #          }}
                                            , ignore=400)
    ids = []
    for doc in docs_list:
        id = doc['id']
        es.index(index='researchgate_index', doc_type='paper', id=id, body=doc)
        ids.append(id)
    write_ids(ids)

def collection_vectorize():
    ids = read_ids()
    vectors = []
    for id in ids:
        vectors.append(get_term_vector(es,id))
    vocab = compute_terms(vectors)
    pprint(len(vocab))
    for vector in vectors:
        tf_idf_vector = dict()
        raw_vector = vector['abstract']
        tf_idf_vector['abstract'] = tf_idf_vectorize(vocab, raw_vector, len(vectors))
        raw_vector = vector['title']
        tf_idf_vector['title'] = tf_idf_vectorize(vocab, raw_vector, len(vectors))
        tf_idf_vectors.append(tf_idf_vector)
    pprint(tf_idf_vectors[0])
    return finalize_json_vectors(tf_idf_vectors, ids), vocab
    #return finalize_vectors(tf_idf_vectors, vocab, ids), vocab

def finalize_json_vectors(tf_idf_vectors, ids):
    out_vectors = []
    for i in range(len(tf_idf_vectors)):
        out_vectors.append({'vector':{}, 'id':ids[i]})
    for i in range(len(tf_idf_vectors)):
        vec = tf_idf_vectors[i]
        terms = []
        for term in vec['abstract']:
            terms.append(term)
        for term in vec['title']:
            if term not in vec['abstract']:
                terms.append(term)

        for term in terms:
            a = 0
            b = 0
            if term in vec['title']:
                a = vec['title'][term]
            if term in vec['abstract']:
                b = vec['abstract'][term]
            out_vectors[i]['vector'][term] = a*title_priority + b
    return out_vectors

def finalize_vectors(tf_idf_vectors, vocab, ids):
    out_vectors = []
    for i in range(len(tf_idf_vectors)):
        out_vectors.append({'vector':[], 'id':ids[i]})
    for term in vocab:
        for i in range(len(tf_idf_vectors)):
            a = tf_idf_vectors[i]['title'][term]
            b = tf_idf_vectors[i]['abstract'][term]
            out_vectors[i]['vector'].append(a*title_priority + b)
    return out_vectors
def tf_idf_vectorize(vocab, raw_vector, length):
    tf_idf_vector = dict()

    for term in raw_vector:
        idf = log((length+1)/vocab[term])
        tf = raw_vector[term]['tf']
        tf_idf_vector[term] = idf*tf
    return tf_idf_vector

def compute_terms(vectors):
    vocab = dict()
    for doc_vector in vectors:
        abs_vec = doc_vector['abstract']
        title_vec = doc_vector['title']
        for term in abs_vec:
            if term not in vocab.keys():
                vocab[term] = 1
            else:
                vocab[term] += 1
        for term in title_vec:
            if term not in abs_vec:
                if term not in vocab.keys():
                    vocab[term] = 1
                else:
                    vocab[term] += 1
    return vocab

def get_term_vector(es, doc_id):
    general_vector = es.termvectors(
                                    index = 'researchgate_index',
                                    doc_type = 'paper',
                                    id = doc_id,
                                    field_statistics = True,
                                    fields=['abstract','title'],
                                    term_statistics = True
                                )
    result = dict()
    result['abstract'] = vectorize(general_vector, 'abstract')
    result['title'] = vectorize(general_vector, 'title')
    return result

def vectorize(general_vector, type):
    temp= dict()
    curr_termvec = general_vector["term_vectors"][type]["terms"]
    tokens = curr_termvec.keys()
    for token in tokens:
        temp.update({token : {'tf':curr_termvec[token]["term_freq"]}})
    return temp

def load_docs():
    docs = []
    path = os.path.join(os.path.dirname(__file__).replace('elastic', ''), 'all_jsons')
    print(path)
    for filename in os.listdir(path):
        with open(path + '/' + filename, 'r') as f:
            doc = dict()
            real_doc = json.loads(f.read())
            authors = real_doc['datas']['authors'].values()
            doc['authors'] = ''
            for author in authors:
                doc['authors'] += author + ' , '
            doc['abstract'] = real_doc['datas']['abstract']
            doc['title'] = real_doc['datas']['title']
            doc['id'] = real_doc['datas']['publication_uid']
            docs.append(doc)
    return docs
def write_ids(ids):
    with open('../ids.txt', 'wb') as f:
        pickle.dump(ids, f)
def read_ids():
    with open('../ids.txt', 'rb') as f:
        ids = pickle.load(f)
    return ids

def write_vectors(vectors):
    with open('../vectors.txt', 'wb') as f:
        pickle.dump(vectors, f)

def main():
    #load_docs()
    print('hello')
    index()
    #vectors = collection_vectorize()
    #write_vectors(vectors)

if __name__ == '__main__':
    main()