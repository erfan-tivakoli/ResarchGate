__author__ = 'Rfun'


def get_uid_from_url(page_url):
    return (page_url.split('/')[-1]).split('_')[0]

def get_name_by_url(author_url):
    author_id = get_uid_from_url(author_url)
    underlined_name = author_url.split(author_id)[1]
    spaced_name = underlined_name.replace('_',' ')
    author_name = spaced_name.strip()

    return author_name