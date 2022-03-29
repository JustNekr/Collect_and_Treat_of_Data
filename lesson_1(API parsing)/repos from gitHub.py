import json
import requests

"""
правда много дополнительной инфы по репозиторию подтягивается
"""


username = input("Enter the github username:")
request = requests.get(f'https://api.github.com/users/{username}/repos')
response = request.json()


with open(f'{username}.json', 'w') as f:
    json.dump(response, f)

# на всякий случай вывод названий сделал
with open(f'{username}.json', 'r') as x:
    data = json.load(x)
    print(type(data))
    for i in data:
        print(i['name'])


