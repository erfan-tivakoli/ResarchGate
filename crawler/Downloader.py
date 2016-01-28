__author__ = 'Rfun'

import requests
import json
from pprint import pprint
import traceback
from crawler.utils import *


def download_url(page_url):
    result = {}

    headers = {
        'accept': 'application/json',
        'x-requested-with': 'XMLHttpRequest'
    }

    try:
        pprint('started to fetch %s' % page_url)
        r = requests.get(page_url)
        publication_uid = get_uid_from_url(page_url)
        result['publication_uid'] = publication_uid

        result['page'] = r.content

        js_cited_in_url = "https://www.researchgate.net/publicliterature.PublicationIncomingCitationsList.html?publicationUid=" \
                          + str(publication_uid) + \
                          "&showCitationsSorter=true&showAbstract=true&showType=true&showPublicationPreview=true&" \
                          "swapJournalAndAuthorPositions=false&limit=100000"

        pprint('started to fetch the cited in')
        r = requests.get(js_cited_in_url, headers=headers)
        result['cited_in'] = json.loads(r.text)

        pprint('started to fetch the references')
        js_references_url = "https://www.researchgate.net/publicliterature.PublicationCitationsList.html?publicationUid=" \
                            + str(publication_uid) + \
                            "&showCitationsSorter=true&showAbstract=true&showType=true&showPublicationPreview=true&" \
                            "swapJournalAndAuthorPositions=false&limit=10000"
        r = requests.get(js_references_url, headers=headers)
        result['references'] = json.loads(r.text)

        pprint('finished fetching the total page')
        return result
    except:
        print('Error in request: ')
        traceback.print_exc()



def main():
    page_url = 'https://www.researchgate.net/publication/282570552_A_Bayesian_approach_to_constrained_single-_and_multi-objective_optimization'
    result = (download_url(page_url))


if __name__ == '__main__':
    main()