import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient


req_vacancy = input('введите название искомой вакансии: ')

client = MongoClient('localhost', 27017)
db = client["vacancies"]


def find_job(required_vacancy):
    vacancies = []

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/94.0.4606.61 Safari/537.36'}
    url = 'https://hh.ru/'
    params = {'fromSearchLine': 'true',
              'st': 'searchVacancy',
              'text': required_vacancy,
              'from': 'suggest_post',
              'page': 0}   # еачинается с 0

    while True:
        response = requests.get(url + 'search/vacancy', params=params, headers=headers)

        soup = bs(response.text, 'html.parser')
        vacancy_list = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})

        if not vacancy_list or not response.ok:
            break

        for vacancy in vacancy_list:

            vacancy_name = vacancy.find('a', attrs={'class': 'bloko-link'}).text
            vacancy_link = vacancy.find('a', attrs={'class': 'bloko-link'})['href']
            # print(type(vacancy_link))

            compensation_block = vacancy.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
            vacancy_compensation = {'Min': None,
                                    'Max': None,
                                    'currency': None}
            if compensation_block:
                compensation_list = compensation_block.contents
                compensation_list = [i for i in compensation_list if i != ' ']
                vacancy_compensation['currency'] = compensation_list.pop(-1).replace('.', '')
                if compensation_list[0] == 'от ':
                    vacancy_compensation['Min'] = float(compensation_list[1].replace('\u202f', ''))
                elif compensation_list[0] == 'до ':
                    vacancy_compensation['Max'] = float(compensation_list[1].replace('\u202f', ''))
                else:
                    compensation_list = compensation_list[0].replace('\u202f', '').split(' – ')
                    vacancy_compensation['Min'] = float(compensation_list.pop(0))
                    vacancy_compensation['Max'] = float(compensation_list.pop(0))

            vacancy_dict = {'vacancy_name': vacancy_name,
                            'vacancy_compensation': vacancy_compensation,
                            'vacancy_link': vacancy_link,
                            'site_link': url}

            vacancies.append(vacancy_dict)
            db.head_hunter.update_one({'vacancy_link': vacancy_link}, {'$set': vacancy_dict}, upsert=True)
        params['page'] += 1
    # db.head_hunter.insert_many(vacancies)
    # with open('vacansies_hh.json', 'w', encoding='utf-8') as file:
    #     json.dump(vacancies, file)


if __name__ == '__main__':
    find_job(req_vacancy)
