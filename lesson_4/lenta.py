from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client["news"]

url = 'https://lenta.ru'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/94.0.4606.61 Safari/537.36'}

response = requests.get(url)
dom = html.fromstring(response.text)

items = dom.xpath("//div[contains(@class, 'b-yellow-box')]/div[contains(@class, 'item')]")

news_list = []

for item in items:
    link = item.xpath(".//a/@href")[0]
    if link.startswith('/news'):  # отсеиваю рекламу
        response = requests.get(url + link)
        dom = html.fromstring(response.text)

        news_name = dom.xpath("//div[contains(@class, 'b-topic__title-yandex')]/text()")[0]
        news_date = dom.xpath("//div[contains(@class, 'b-topic')]/time[@class='g-date']/@datetime")[0]

        news = {
            'source_name': 'lenta.ru',
            'news_name': news_name,
            'news_link': url,
            'news_date': news_date,
        }
        db.lenta.update_one({'news_link': url}, {'$set': news}, upsert=True)
        news_list.append(news)


pprint(news_list)


