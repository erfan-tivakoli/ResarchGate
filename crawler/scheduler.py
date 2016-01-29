__author__ = 'Rfun'
import queue
from queue import Queue
from pprint import pprint


class Scheduler():
    def __init__(self, initial_urls):
        self.history = set({})
        self.initial_urls = initial_urls
        # initial_urls is None:
        #     self.initial_urls = [
        #         'https://www.researchgate.net/publication/267960550_ImageNet_Classification_'
        #         'with_Deep_Convolutional_Neural_Networks']

        self.q = queue.Queue(maxsize=0)
        for link in self.initial_urls:
            self.q.put(link)
            self.history.add(link)

    def check_duplication(self, new_url):
        if new_url in self.history:
            # print('the link %s is duplicated' % (new_url))
            return True
        return False

    def add(self, urls):
        for url in urls:
            print('adding url %s to scheduler' %url)
            if not self.check_duplication(url):
                # pprint('adding url %s to the queue' % url)
                self.q.put(url)
                self.history.add(url)


    def get_new_url(self):
        try:
            return self.q.get()
        except queue.Empty:
            # print('The scheduler is empty')
            pass


def main():
    a = Scheduler()


if __name__ == '__main__':
    main()