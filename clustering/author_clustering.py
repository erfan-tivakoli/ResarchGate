import json
import os
from pprint import pprint
from clustering.kmeans import clustering

__author__ = 'chester'

#def load_authors():

number_of_authors = 100

def load_authors():
    path = os.path.join(os.path.dirname(__file__).replace('clustering', ''), 'authors')
    authors = []
    for filename in os.listdir(path):
        with open(path + '/' + filename, 'r') as f:
            real_author= json.loads(f.read())
            author = dict()
            author['name'] = real_author['author_name']
            author['vector'] = dict()
            uids = real_author['publications']
            uids.pop('number_of_pages')
            for uid in uids:
                author['vector'][uid] = 1
            authors.append(author)
                #uid_authors = uids[uid]
                #ack = False
                #for i in range(len(uid_authors)):
                #    uid_author = uid_authors[i]
                #    if uid_author[0] ==  author['name']:
                #        ack = True
                #        author['vector'][uid] = 1
                #if not ack:
                #    print('ERROR--ERROR--ERROR--ERROR--ERROR--ERROR--ERROR')
    return authors

def author_clustering(authors):
    clusters = clustering(authors)
    cluster = clusters['cluster_1']['cluster']
    clustering_authors = dict()
    for i in range(len(cluster)):
        if cluster[i] not in clustering_authors:
            clustering_authors[cluster[i]] = []
        clustering_authors[cluster[i]].append(authors[i]['name'])
    return clustering_authors

def main():
    authors = (load_authors())

if __name__ == '__main__':
    main()

