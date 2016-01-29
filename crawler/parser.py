from crawler.utils import get_uid_from_url

__author__ = 'chester'

from bs4 import BeautifulSoup
import requests
from pprint import pprint
import traceback

base_url = "https://www.researchgate.net/"

def parse_author_page_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    number_of_pages = 1
    try:
        pages_link = soup.select('.c-list-navi')[0].select('.navi-page-link')
        number_of_pages = int(pages_link[len(pages_link)-1].text)
    except:
        print('has no pages')
        number_of_pages = 1
    items = (soup.select('.li-publication'))
    papers = dict()
    for item in items:
        url = item.select('.publication-preview')[0].get('href')
        uid = get_uid_from_url(url)
        authors = dict()
        papers[uid] = authors
        author_tags = item.select('a.authors')
        for author_tag in author_tags:
            name = author_tag.text
            link = author_tag.get('href')
            link = 'https://www.researchgate.net/' + link
            authors[name] = link
    result = {'number_of_pages' : number_of_pages, 'publications':papers}
    return result

def parse_html(html, publication_uid):
    soup = BeautifulSoup(html, 'html.parser')
    result = {}
    counter = 0
    ordered_authors = {}

    try:
        abstract_text = soup.select('.pub-abstract')[0].select('div')[1].text
        abstract_text = abstract_text.replace('\n', ' ')
        li_items = soup.select('.publication-detail-author-list')[0].select('li')

        for li in li_items:
            if len(li.select('span')) != 0:
                counter += 1
                ordered_authors[str(counter)] = li.select('span')[0].text

        result['abstract'] = abstract_text
        result['authors'] = ordered_authors
        result['publication_uid'] = publication_uid
        result['title'] = soup.select('.pub-title')[0].text

        return result

    except:
        # print('Error in beautifulsoup: ')
        traceback.print_exc()



def parse_cited_in(json_cited_in):
    result = []
    citation_items = json_cited_in['result']['data']['citationItems']

    for item in citation_items:
        try:
            result += [base_url + item['data']['publicationUrl']]
        except:
            # pprint(json_cited_in['result']['data']['publicationLink'])
            # pprint('cited_in to :')
            # pprint(item['data']['title'])
            pass

    return result


def parse_references(json_references):
    result = []
    citation_items = json_references['result']['data']['citationItems']

    # pprint(json_references)
    for item in citation_items:
        try:
            result += [base_url + item['data']['publicationUrl']]
        except:
            # pprint(json_references['result']['data']['publicationLink'])
            # pprint('referenced to :')
            # pprint(item['data']['title'])
            pass

            traceback.print_exc()

    return result



def parse(result):
    all_datas = {}
    # pprint('parsing html')
    all_datas['datas'] = parse_html(result['page'], result['publication_uid'])
    # pprint('parsing cited_in')
    all_datas['cited_in'] = parse_cited_in(result['cited_in'])
    # pprint('parsing references')
    all_datas['references'] = parse_references(result['references'])
    return all_datas


def main():
    # url = "https://www.researchgate.net/publication/285458515_A_General_Framework_for_Constrained_Bayesian_Optimization_using_Information-based_Search"
    # r = requests.get(url)
    #with open('html.txt', 'r') as f:
    #    html = f.read()
    #parse_html(html, 112)
    #page_url = 'https://www.researchgate.net/profile/Konstantinos_Bousmalis'
    #r = requests.get(page_url)
    #pprint(r.content)
    with open('html.txt', 'r') as f:
        html = f.read()
    pprint(parse_author_page_html(html))



if __name__ == '__main__':
    main()

