__author__ = 'Rfun'

import requests
import json
from pprint import pprint


def download_url(page_url):
    result = {}

    headers = {
        'accept': 'application/json',
        'x-requested-with': 'XMLHttpRequest'
    }

    r = requests.get(page_url)
    publication_uid = (page_url.split('/')[-1]).split('_')[0]

    result['page'] = r.content

    js_cited_in_url = "https://www.researchgate.net/publicliterature.PublicationIncomingCitationsList.html?publicationUid=" \
                      + str(publication_uid) + \
                      "&showCitationsSorter=true&showAbstract=true&showType=true&showPublicationPreview=true&" \
                      "swapJournalAndAuthorPositions=false"

    r = requests.get(js_cited_in_url, headers=headers)
    result['cited_in'] = json.loads(r.text)

    js_references_url = "https://www.researchgate.net/publicliterature.PublicationCitationsList.html?publicationUid=" \
                        + str(publication_uid) + \
                        "&showCitationsSorter=true&showAbstract=true&showType=true&showPublicationPreview=true&" \
                        "swapJournalAndAuthorPositions=false"
    r = requests.get(js_references_url, headers=headers)
    result['references'] = json.loads(r.text)

    return result


def main():
    page_url = "https://www.researchgate.net/publication/" \
               "285458515_A_General_Framework_for_Constrained_Bayesian_Optimization_using_Information-based_Search"
    pprint(download_url(page_url))


if __name__ == '__main__':
    main()
