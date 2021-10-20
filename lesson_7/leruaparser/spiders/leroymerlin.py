import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from lesson_7.leruaparser.items import LeruaparserItem


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']
    # start_urls = ['http://leroymerlin.ru/']

    def __init__(self, query):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}']
        self.query = query

    def parse(self, response: HtmlResponse):
        links = response.xpath("//div[@class='phytpj4_plp largeCard']/a/@href")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruaparserItem(), response=response)
        loader.add_value('link', response.url)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('photo', "//uc-pdp-media-carousel[@slot='media-content']/img/@src")
        loader.add_value('query', self.query)
        loader.add_xpath('price', "//span[@slot='price']/text()")

        return loader.load_item()


