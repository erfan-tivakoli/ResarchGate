__author__ = 'Rfun'

from crawler.Downloader import *
from crawler.parser import *
from crawler.item_pipeline import *
from crawler.scheduler import *

max_articles = 20


def main():
    scheduler = Scheduler()
    item_pipeline = ItemPipeline(scheduler)
    while item_pipeline.get_items_len() < max_articles:
        try:
            next_url = scheduler.get_new_url()
            pprint('next url is %s' % next_url)
            downloaded = download_url(next_url)
            if downloaded is not None:
                parsed = parse(downloaded)
                item_pipeline.add_items(parsed)
                print('now the item len is : %d' % item_pipeline.get_items_len())
        except:
            traceback.print_exc()

    item_pipeline.pickle_graph()
    print(item_pipeline.get_graph())

if __name__ == '__main__':
    main()