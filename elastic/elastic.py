from math import log
from crawler.parser import parse_html

__author__ = 'chester'
from elasticsearch import Elasticsearch
from pprint import pprint

doc_vectors = dict()
es = Elasticsearch()
ids = []
tf_idf_vectors = []
title_priority = 3

def index(docs_list):
    es.indices.delete(index='researchgate_index', ignore=[400, 404])
    es.indices.create(index='researchgate_index', ignore=400)
    for doc in docs_list:
        id = doc['id']
        es.index(index='researchgate_index', doc_type='paper', id=id, body=doc)
        ids.append(id)

def collection_vectorize():
    vectors = []
    for id in ids:
        vectors.append(get_term_vector(es,id))
    vocab = compute_terms(vectors)
    print(vocab)
    for vector in vectors:
        tf_idf_vector = dict()
        raw_vector = vector['abstract']
        tf_idf_vector['abstract'] = tf_idf_vectorize(vocab, raw_vector, len(vectors))
        raw_vector = vector['title']
        tf_idf_vector['title'] = tf_idf_vectorize(vocab, raw_vector, len(vectors))
        tf_idf_vectors.append(tf_idf_vector)
    return finalize_vectors(tf_idf_vectors, vocab, ids)

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
    for term in vocab:
        idf = log((length+1)/vocab[term])
        tf = 0
        if term in raw_vector:
            tf = raw_vector[term]['tf']
        tf_idf_vector[term] = idf*tf
    return tf_idf_vector

def compute_terms(vectors):
    vocab = {}
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
    with open('../crawler/html.txt', 'r') as f:
        html = f.read()
    doc = parse_html(html, 112)
    a = {'id' : 1,'abstract' : 'salam salam saeed xx', 'title' : 'xx salam inja bedoone man'}
    b = {'id' : 2,'abstract' : 'salam hamid', 'title' : 'salam inja bedoone to'}
    c = {'id' : 3,'abstract' : 'salam hamid', 'title' : 'salam inja bedoone to'}
    return [a,b,c]

def main():
    docs = load_docs()
    index(docs)
    pprint(collection_vectorize())


if __name__ == '__main__':
    main()