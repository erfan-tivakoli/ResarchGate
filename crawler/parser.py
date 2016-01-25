__author__ = 'chester'

from bs4 import BeautifulSoup
import requests
from pprint import pprint

base_url = "https://www.researchgate.net/"


def parse_html(html, publication_uid):
    soup = BeautifulSoup(html, 'html.parser')
    abstract_text = soup.select('.pub-abstract')[0].select('div')[1].text
    abstract_text = abstract_text.replace('\n', ' ')
    result = {}
    li_items = soup.select('.publication-detail-author-list')[0].select('li')
    counter = 0
    ordered_authors = {}

    for li in li_items:
        if len(li.select('span')) != 0:
            counter += 1
            ordered_authors[str(counter)] = li.select('span')[0].text

    result['abstract'] = abstract_text
    result['authors'] = ordered_authors
    result['id'] = publication_uid
    result['title'] = soup.select('.pub-title')[0].text
    return result


def parse_cited_in(json_cited_in):
    result = []
    citation_items = json_cited_in['result']['data']['citationItems']

    for item in citation_items:
        result += [base_url + item['data']['publicationUrl']]

    return result


def parse_references(json_references):
    result = []
    citation_items = json_references['result']['data']['citationItems']

    for item in citation_items:
        result += [base_url + item['data']['publicationUrl']]

    return result


def parse(result):
    all_datas = {}
    all_datas['datas'] = parse_html(result['page'])
    all_datas['cited_in'] = parse_cited_in(result['cited_in'])
    all_datas['references'] = parse_cited_in(result['references'])
    return all_datas


def main():
    # url = "https://www.researchgate.net/publication/285458515_A_General_Framework_for_Constrained_Bayesian_Optimization_using_Information-based_Search"
    # r = requests.get(url)
    with open('html.txt', 'r') as f:
        html = f.read()
    parse_html(html)


if __name__ == '__main__':
    main()

