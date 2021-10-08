from pprint import pprint
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
urls = []
news_list = []

print(len(items))
for item in items:
    link = item.xpath(".//a/@href")[0]
    print(link)
    # if link.startswith('/news'):  # отсеиваю рекламу
    #     urls.append(url + link)