import json
import re

from env import PASS, LOGIN
import scrapy
from scrapy.http import HtmlResponse




class InstaspiderSpider(scrapy.Spider):
    name = 'InstaSpider'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']

    def parse(self, response):
        x = response.follow()
        pass


    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')