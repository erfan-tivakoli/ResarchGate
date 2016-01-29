import json
import os
import pickle
from pprint import pprint
from elastic import search

__author__ = 'chester'



def main():
    with open('../clustering/clustering_labels.txt', 'rb') as file:
        labels = pickle.load(file)
    with open('../clustering/clustering.json', 'r') as f:
        cluster_info = json.load(f)['cluster_2']['cluster']
    with open('../ids.txt', 'rb') as ids_f:
        ids = pickle.load(ids_f)
    while True:
        print('-1-Show paper')
        print('-2-Search')
        print('-3-show clusters')
        print('-4-Exit')
        choice = input('Enter # : ')
        if choice == '1':
            uid = input('Enter UID : ')
            with open('../all_jsons/' + uid + '.json', 'r') as f:
                    real_doc = json.loads(f.read())
                    #print(real_doc)
                    print('\nTitle : ')
                    pprint(real_doc['datas']['title'])
                    print('\nAbstract : ')
                    pprint(real_doc['datas']['abstract'])
                    print('\nAuthors : ')
                    authors = real_doc['datas']['authors']
                    for i in authors:
                        print(' ' + authors[i])
                    print_dash()
        elif choice == '2':
            print('Search :')
            query = input('Enter your query: ')
            has_clustering = input('do you want clustering? Y/N')
            if(has_clustering == 'Y'):
                print_dash()
                for i in range(len(labels)):
                    label = labels[i]
                    label_str = ''
                    for term in label:
                        label_str += term + ' '
                    print('topic : ' + str(i+1))
                    print(' - ' + label_str)
                    print_dash()
                cluster_num = int(input('choose # of topic : '))-1
                results = search.search(query, 1000)
                no_result = True
                for res in results:
                    index = ids.index(res[0])
                    if cluster_info[index] == cluster_num :
                        no_result = False
                        print('page rank : ' + str(res[1]['page_rank']) + '\t' + 'publication UID : ' + str(res[0]) +   '\t' + 'score : ' + str(res[1]['score']))
                        print('Title : ' + str(res[1]['title']) + '\n')
                        print_dash()
                if no_result :
                    print('\nno paper is found')
                    print_dash()

            else:
                print('-1-top ten')
                print('-2-all')
                all_choice = input('--Enter :  ')
                if(all_choice == '1'):
                    print_dash()
                    results = search.search(query, 10)
                    for res in results:
                        print('page rank : ' + str(res[1]['page_rank']) + '\t' + 'publication UID : ' + str(res[0]) +   '\t' + 'score : ' + str(res[1]['score']) + '\n')
                        pprint('Title : ' + str(res[1]['title']) + '\n')
                        pprint('abstract : ' + str(res[1]['abstract']))
                        print_dash()
                else:
                    print_dash()
                    results = search.search(query, 1000)
                    for res in results:
                        print('page rank : ' + str(res[1]['page_rank']) + '\t' + 'publication UID : ' + str(res[0]) +   '\t' + 'score : ' + str(res[1]['score']) + '\n')
                        print('Title : ' + str(res[1]['title']) + '\n')
                        print_dash()
        elif choice == '3':
            print_dash()
            for i in range(len(labels)):
                label = labels[i]
                label_str = ''
                for term in label:
                    label_str += term + ' '
                print('topic : ' + str(i+1))
                print(' - ' + label_str)
                print_dash()
            cluster_number = int(input('choose cluster to show : '))-1
            for i in range(len(cluster_info)):
                if cluster_info[i] == cluster_number:
                    uid = ids[i]
                    with open('../all_jsons/' + uid + '.json', 'r') as f:
                        real_doc = json.loads(f.read())
                        print('UID : ' + str(uid) + '\n')
                        print('Title : ')
                        print(real_doc['datas']['title'])
                        print_dash()
        elif choice == '4':
            break

def print_dash():
    print('---------------------------------------------------------------------')
if __name__ == '__main__':
    main()

