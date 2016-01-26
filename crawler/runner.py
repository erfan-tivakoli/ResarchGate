__author__ = 'Rfun'

from crawler.downloader import *
from crawler.parser import *
from crawler.item_pipeline import *
from crawler.scheduler import *

max_articles = 10

def main():
    scheduler = Scheduler()
    item_pipeline = ItemPipeline(scheduler)
    while(item_pipeline.get_items_len() < 20):
        next_url = scheduler.get_new_url()
        downloaded = download_url(next_url)
        parsed = parse(downloaded)
        item_pipeline.add_items(parsed)

if __name__ == '__main__':
    main()