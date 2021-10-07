from pprint import pprint

from pymongo import MongoClient

interest_compensation = float(input('какая ЗП интересует в рублях: '))
usd_to_rub = 72.14
client = MongoClient('localhost', 27017)
db = client["vacancies"]

vacancies = db.head_hunter.find(
    {'$or':
        [
            {'$and':
                [
                    {'vacancy_compensation.currency': 'руб'},
                    {'$or':
                        [
                            {'vacancy_compensation.Min': {'$gte': interest_compensation}},
                            {'vacancy_compensation.Max': {'$gt': interest_compensation}}
                        ]
                    }
                ]
            },
            {'$and':
                [
                    {'vacancy_compensation.currency': 'USD'},
                    {'$or':
                        [
                            {'vacancy_compensation.Min': {'$gte': interest_compensation / usd_to_rub}},
                            {'vacancy_compensation.Max': {'$gt': interest_compensation / usd_to_rub}}
                        ]
                    }
                ]
            }
        ]
    },
    {'_id': False, 'site_link': False}
)


for doc in vacancies:
    pprint(doc)
