__author__ = 'Rfun'


def get_uid_from_url(page_url):
    return (page_url.split('/')[-1]).split('_')[0]