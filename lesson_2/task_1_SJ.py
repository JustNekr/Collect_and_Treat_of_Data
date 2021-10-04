import json
import re
import requests
from bs4 import BeautifulSoup as bs


req_vacancy = input('введите название искомой вакансии: ')


def find_job(required_vacancy):
    vacancies = []
    url = 'https://russia.superjob.ru'
    params = {'keywords': required_vacancy,
              'page': 1}  # начинается с 1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/94.0.4606.61 Safari/537.36'}

    while True:
        response = requests.get(url + '/vacancy/search/', params=params, headers=headers)
        soup = bs(response.text, 'html.parser')

        vacancy_list = soup.find_all('div', attrs={'class': 'jNMYr GPKTZ _1tH7S'})
        if not vacancy_list or not response.ok:
            break

        for i in vacancy_list:
            vacancy_name = i.contents[0].text
            vacancy_link = url + i.find('a')['href']

            vacancy_compensation = {'Min': None,
                                    'Max': None,
                                    'currency': None}
            # vacancy_compensation_min = None
            # vacancy_compensation_max = None
            # vacancy_compensation_currency = None

            vacancy_compensation_text = i.find('span', attrs={'class': '_1h3Zg _2Wp8I _2rfUm _2hCDz _2ZsgW'}).text.replace(
                '\u00a0', '')

            currency = re.findall(r'\d+(\w+).$', vacancy_compensation_text)   # не встретил ни одной вакансии в иной валюте
            # на SuperJob
            if len(currency) == 1:
                vacancy_compensation['currency'] = currency[0]
                # vacancy_compensation_currency = currency[0]

            if re.match(r'\d', vacancy_compensation_text):
                value = re.findall(r'\d+', vacancy_compensation_text)
                vacancy_compensation['Min'] = float(value[0])
                # vacancy_compensation_min = float(value[0])
                if len(value) > 1:
                    vacancy_compensation['Max'] = float(value[1])
                    # vacancy_compensation_max = float(value[1])
                else:
                    vacancy_compensation['Max'] = float(value[0])
                    # vacancy_compensation_max = float(value[0])
            elif vacancy_compensation_text.startswith('от'):
                vacancy_compensation['Min'] = float(re.findall(r'\d+', vacancy_compensation_text)[0])
                # vacancy_compensation_min = float(re.findall(r'\d+', vacancy_compensation_text)[0])
            elif vacancy_compensation_text.startswith('до'):
                vacancy_compensation['Max'] = float(re.findall(r'\d+', vacancy_compensation_text)[0])
                # vacancy_compensation_max = float(re.findall(r'\d+', vacancy_compensation_text)[0])

            vacancy_dict = {'vacancy_name': vacancy_name,
                            'vacancy_link': vacancy_link,
                            'site_link': url,
                            'vacancy_compensation': vacancy_compensation,
                            # 'vacancy_compensation_min': vacancy_compensation_min,
                            # 'vacancy_compensation_max': vacancy_compensation_max,
                            # 'vacancy_compensation_currency': vacancy_compensation_currency
                            }

            vacancies.append(vacancy_dict)
        params['page'] += 1

    with open('vacansies_sj.json', 'w', encoding='utf-8') as file:
        json.dump(vacancies, file)


if __name__ == '__main__':
    find_job(req_vacancy)
