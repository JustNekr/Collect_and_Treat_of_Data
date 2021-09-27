import json
import requests
from access import a_t
from access import u_i

user_id = u_i
access_token = a_t

url = 'https://api.vk.com/method/'
METHOD = 'friends.get'
order = 'hints'
count = 10
fields = 'first_name'
# любопытно, что если не указывать поля, то возвращаются только id-шники, но если указать хотя
# бы одно, то подтягиваются все которые по умолчанию

v = 5.131


request = requests.get(f'{url}{METHOD}?user_id={user_id}&order={order}&count={count}&fields={fields}&access_token'
                       f'={access_token}&v={v}')
response = request.json()

'''
сохраняю в файл, как написанно в задании
'''
with open(f'Friends of {user_id}.json', 'w') as f:
    json.dump(response, f)

'''
вывод имен для наглядности
'''
for i in response['response']['items']:
    print(i['first_name'])

