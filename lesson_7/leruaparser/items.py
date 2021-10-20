# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from pprint import pprint

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Identity
from scrapy.pipelines.images import ImagesPipeline


def clear_price(price):
    price = float(price.replace(' ', ''))
    return price


class LeruaparserItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    photo = scrapy.Field(output_processor=Identity())
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(clear_price), output_processor=TakeFirst())
    query = scrapy.Field(output_processor=TakeFirst())
    # price = scrapy.Field(output_processor=TakeFirst())

    _id = scrapy.Field()
