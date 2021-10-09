import re
from datetime import datetime, timedelta
from pprint import pprint

from lxml import html
import requests
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client["news"]

url = 'https://yandex.ru/news/'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/94.0.4606.61 Safari/537.36'}

response = requests.get(url)
dom = html.fromstring(response.text)

items = dom.xpath("//div[contains(@class, 'mg-grid__row')]/div[contains(@class, 'mg-grid__col')]/article")

for item in items:

    source_name = item.xpath(".//div[contains(@class, 'source_dot')]/span/a/text()")[0]
    news_name = item.xpath(".//h2/text()")[0].replace('\xa0', ' ')
    link = item.xpath(".//div[contains(@class, 'source_dot')]/span/a/@href")[0]
    news_date = item.xpath(".//div[contains(@class, 'source_dot')]/span[contains(@class, 'time')]/text()")[0]
    if news_date.startswith('вчера'):
        news_date = re.search(r"(\d+.\d+)", news_date).group(0)
        Z = datetime.now() - timedelta(days=1)
        news_date = f'{(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d%Z")}T{news_date}:00{datetime.today().strftime("%z")}'
    else:
        news_date = f'{datetime.now().strftime("%Y-%m-%d%Z")}T{news_date}:00{datetime.today().strftime("%z")}'
        # не могу понять почему часовой пояс не прилепляется

    news = {
            'source_name': source_name,
            'news_name': news_name,
            'news_link': link,
            'news_date': news_date,
        }
    db.yandex.update_one({'news_link': link}, {'$set': news}, upsert=True)



