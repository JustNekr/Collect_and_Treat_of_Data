from lxml import html
import requests
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client["news"]

url = 'https://news.mail.ru/'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/94.0.4606.61 Safari/537.36'}

response = requests.get(url)
dom = html.fromstring(response.text)

items = dom.xpath("//div[contains(@class,'daynews__item')]|//ul[@data-module='TrackBlocks']/li[@class='list__item']")


for item in items:
    link = item.xpath(".//a/@href")[0]
    response_news = requests.get(link)
    dom_news = html.fromstring(response_news.text)

    news_name = dom_news.xpath("//div[contains(@class, 'article__intro')]/p/text()")[0].replace('\xa0', ' ')
    source_name = dom_news.xpath("//span[contains(@class, 'breadcrumbs__item')]/span/a/@href")[0]
    news_date = dom_news.xpath("//span[contains(@class, 'breadcrumbs__item')]/span/span/@datetime")[0]

    news = {
        'source_name': source_name,
        'news_name': news_name,
        'news_link': link,
        'news_date': news_date,
    }
    db.mail.update_one({'news_link': link}, {'$set': news}, upsert=True)

