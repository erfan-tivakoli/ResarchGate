__author__ = 'Rfun'
from crawler.downloader import *
from crawler.parser import *

def main():
    page_url = "https://www.researchgate.net/publication/227183327_Development_Density-Based_Optimization_Modeling_of_Sustainable_Land_Use_Patterns"
    result = download_url(page_url)
    all_links = parse(result)
    pprint(all_links)

if __name__ == '__main__':
    main()