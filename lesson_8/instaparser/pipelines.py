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
        print()
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
        item['photo'] = [itm[1] for itm in results if itm[0]]
        return item
