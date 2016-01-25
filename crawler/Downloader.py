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
    result['publication_uid'] = publication_uid

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
    page_url = "https://www.researchgate.net/publication/227183327_Development_Density-Based_Optimization_Modeling_of_Sustainable_Land_Use_Patterns"
    result = (download_url(page_url))
    pprint(result)
    print ((result['cited_in']['result']['data']['citationItems'][0]['data']['publicationUrl']))


if __name__ == '__main__':
    main()