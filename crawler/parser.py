__author__ = 'chester'

from bs4 import BeautifulSoup
import requests
from pprint import pprint
def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    print((soup.select('.pub-abstract')[0]).)

def main():
    #url = "https://www.researchgate.net/publication/285458515_A_General_Framework_for_Constrained_Bayesian_Optimization_using_Information-based_Search"
    #r = requests.get(url)
    with open('html.txt','r') as f:
        html = f.read()
    parse_html(html)
if __name__ == '__main__':
    main()

