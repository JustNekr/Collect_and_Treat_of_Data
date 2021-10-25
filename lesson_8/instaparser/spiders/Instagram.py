import json
import re

from env import PASSWORD, LOGIN
import scrapy
from scrapy.http import HtmlResponse


class InstaSpider(scrapy.Spider):
    name = 'InstaSpider'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']

    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'

    inst_login = LOGIN
    inst_pwd = PASSWORD

    followers_url = 'https://www.instagram.com/morozik_ivan/followers/'
    following_url = 'https://www.instagram.com/morozik_ivan/following/'

    user_for_parse = 0

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.login,
            formdata={'username': self.inst_login,
                      'enc_password': self.inst_pwd},
            headers={'x-csrftoken': csrf}
        )

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            yield response.follow(
                self.followers_url,
                callback=self.followers_parse,
                cb_kwargs={'username': self.user_for_parse}
            )

    def followers_parse(self, response: HtmlResponse):
        otvet = response
        print()
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