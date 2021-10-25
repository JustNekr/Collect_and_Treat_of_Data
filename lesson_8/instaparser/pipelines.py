import re

import scrapy
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class InstaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.instagram

    def process_item(self, item, spider):
        # collection = self.mongo_base[item['query']]
        # collection.update_one({'link': item['link']}, {'$set': item}, upsert=True)
        return item


class InstaImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            try:
                yield scrapy.Request(item['photo'])
            except Exception as e:
                print(e)

    def item_completed(self, results, item, info):
        print()
        pass

    # def file_path(self, request, response=None, info=None, *, item=None):
    #     origin = super(LeruaImagesPipeline, self).file_path(request)
    #     return f"{item['query']}/{origin}"
