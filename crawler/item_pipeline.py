__author__ = 'Rfun'
import json

class ItemPipeline():

    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.all_items = set({})

    def add_items(self, all_datas):
        self.dump_json(all_datas)
        self.scheduler.add(all_datas['cited_in'] + all_datas['references'])

    def dump_json(self,result):
        json_format = json.dump(result)
        self.all_items.add(json_format)


    def get_items_len(self):
        return len(self.all_items)