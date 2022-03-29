from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from lesson_7.leruaparser.spiders.leroymerlin import LeroymerlinSpider
from lesson_7.leruaparser import settings


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)

    query = input('что ищем?')
    process.crawl(LeroymerlinSpider, query=query)
    process.start()
