import json
import os
from pprint import pprint
from clustering.kmeans import clustering

__author__ = 'chester'

#def load_authors():

number_of_authors = 100

def load_papers():
    path = os.path.join(os.path.dirname(__file__).replace('clustering', ''), 'all_jsons')
    print(path)
    users = dict()
    for filename in os.listdir(path):
        with open(path + '/' + filename, 'r') as f:
            real_doc = json.loads(f.read())
            authors = real_doc['datas']['authors']
            id = real_doc['datas']['publication_uid']
            for i in authors:
                if authors[i] not in users:
                    users[authors[i]] = dict()
                index = int(i)
                print(index)
                users[authors[i]][id] = index
    return users

def main():
    authors = (load_papers())
    pprint(clustering(authors))

if __name__ == '__main__':
    main()

