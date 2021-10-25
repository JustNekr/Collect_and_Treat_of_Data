import json
import re
from copy import deepcopy
from urllib.parse import urlencode

from .env import PASSWORD, LOGIN
import scrapy
from scrapy.http import HtmlResponse

from ..items import InstaparserItem


class InstaSpider(scrapy.Spider):
    name = 'InstaSpider'
    allowed_domains = ['instagram.com', 'i.instagram.com']
    start_urls = ['http://instagram.com/']

    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'

    inst_login = 'justnekr@gmail.com'
    inst_pwd = '#PWD_INSTAGRAM_BROWSER:9:1635163985:AVdQAEXPdtt+ORZ2GGEO1vCVmliYrbPrvDkWDBpgePJDnPxWIH8K0hYoAtUPwscTgz1sSk6rmt6GfMQ0Hsi71rw2xSXeJ2FCB1N3uBEkAVMpjikrTJe9ywVEl2u+uAzUUbhAM51VbWfyOWJM9w=='

    users_for_parse = ['morozik_ivan']
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
                f'/{self.users_for_parse[0]}',
                callback=self.user_parse,
                cb_kwargs={'username': self.users_for_parse[0]}
            )

    def user_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        print()

        variables = {'count': 12,
                     'search_surface': 'follow_list_page'}
        url_posts = f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?{urlencode(variables)}'

        yield response.follow(url_posts,
                              callback=self.followers_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)}
                              )


    def followers_parse(self, response, username, user_id, variables):
        j_data = response.json()
        users = j_data.get('users')
        for user in users:
            item = InstaparserItem(
                user_id=user.get('pk'),
                username=user.get('username'),
                photo=user.get('profile_pic_url'),
                full_name=user.get('full_name'),
                )
            yield item
        if j_data.get('big_list'):
            variables['max_id'] = j_data.get('next_max_id')
            next_url = f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?{urlencode(variables)}'
            yield response.follow(next_url,
                                  callback=self.followers_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables)}
                                  )




    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')