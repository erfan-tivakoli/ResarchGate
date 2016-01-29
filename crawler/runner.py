__author__ = 'Rfun'

from crawler.Downloader import *
from crawler.parser import *
from crawler.item_pipeline import *
from crawler.scheduler import *

max_articles = 1000
max_authors = 500

def crawl_articles():
    scheduler = Scheduler()
    item_pipeline = ItemPipeline(scheduler)
    while item_pipeline.get_items_len() < max_articles:
        print('\r %% %.2 of the total work' %(item_pipeline.get_items_len()*100/max_articles))
        try:
            next_url = scheduler.get_new_url()
            # pprint('next url is %s' % next_url)
            downloaded = download_url(next_url)
            if downloaded is not None:
                parsed = parse(downloaded)
                item_pipeline.add_items(parsed)
                # print('now the item len is : %d' % item_pipeline.get_items_len())
        except:
            traceback.print_exc()

    item_pipeline.save_to_text_file()
    item_pipeline.pickle_graph()

def crawl_author():
    initial_urls = ["https://www.researchgate.net/researcher/8159937_Zoubin_Ghahramani"]
    scheduler = Scheduler(initial_urls)
    item_pipeline = ItemPipeline(scheduler)

    while item_pipeline.get_items_len() < max_authors:
        try:
            next_url = scheduler.get_new_url()
            print('started %s' %next_url)
            downloaded = download_author(next_url)
            print('downloaded')
            if downloaded is not None:
                print('we are adding')
                item_pipeline.add_authors(downloaded)
                print('added')
        except:
            pass

def main():
    # crawl_articles()
    crawl_author()
    # print(item_pipeline.get_graph())

if __name__ == '__main__':
    main()