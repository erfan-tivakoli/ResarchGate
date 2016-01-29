import json
import os
from pprint import pprint
from clustering.kmeans import clustering

__author__ = 'chester'

#def load_authors():

number_of_authors = 100

def load_papers():
    path = os.path.join(os.path.dirname(__file__).replace('clustering', ''), 'all_jsons')
    authors = []
    for filename in os.listdir(path):
        with open(path + '/' + filename, 'r') as f:
            real_author= json.loads(f.read())
            author = dict()
            author['name'] = real_author['name']
            author['vector'] = dict()
            uids = real_author['publications']
            for uid in uids:
                uid_authors = uids[uid]
                
                for i in range(len(uid_authors)):
                    uid_author = uid_authors[i]
                    if uid_author[0] ==  author['name']:
                        author['vector'][uid] = i+1

    return authors

def main():
    authors = (load_papers())
    pprint(clustering(authors))

if __name__ == '__main__':
    main()

