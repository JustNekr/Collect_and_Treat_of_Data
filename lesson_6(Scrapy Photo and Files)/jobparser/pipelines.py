# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pprint import pprint

from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.scrapy_vacancy

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['link'] = self.process_link(item['link'])
            item['salary'] = self. process_salary_hh(item['salary'])
        if spider.name == 'sjru':
            item['salary'] = self.process_salary_sj(item['salary'])
        collection = self.mongo_base[spider.name]
        collection.update_one({'link': item['link']}, {'$set': item}, upsert=True)
        return item

    def process_salary_sj(self, salary):
        compensation_dict = {'Min': None,
                             'Max': None,
                             'currency': None,
                             'comment': None}
        salary = [i for i in salary if i != '\xa0']

        if salary[0] == 'от':
            salary_list = salary[1].split('\xa0')
            compensation_dict['currency'] = salary_list.pop(-1)
            compensation_dict['Min'] = float(''.join(salary_list))
        elif salary[0] == 'до':
            salary_list = salary[1].split('\xa0')
            compensation_dict['currency'] = salary_list.pop(-1)
            compensation_dict['Max'] = float(''.join(salary_list))
        else:
            if len(salary) == 2:
                compensation_dict['currency'] = salary.pop(-1)
                compensation_dict['Min'] = float(salary[0].replace('\xa0', ''))
                compensation_dict['Max'] = float(salary[0].replace('\xa0', ''))
            elif len(salary) == 3:
                compensation_dict['currency'] = salary.pop(-1)
                compensation_dict['Min'] = float(salary[0].replace('\xa0', ''))
                compensation_dict['Max'] = float(salary[1].replace('\xa0', ''))

        return compensation_dict


    def process_salary_hh(self, salary):
        compensation_dict = {'Min': None,
                             'Max': None,
                             'currency': None,
                             'comment': None}
        salary = [i for i in salary if i != ' ']
        if len(salary) > 1:
            compensation_dict['comment'] = salary.pop(-1)
            compensation_dict['currency'] = salary.pop(-1)
            if len(salary) == 4:
                compensation_dict['Min'] = float(salary[1].replace('\xa0', ''))
                compensation_dict['Max'] = float(salary[3].replace('\xa0', ''))
            else:
                if salary[0] == 'от ':
                    compensation_dict['Min'] = float(salary[1].replace('\xa0', ''))
                elif salary[0] == 'до ':
                    compensation_dict['Max'] = float(salary[1].replace('\xa0', ''))

        return compensation_dict

    def process_link(self, link):
        link = link.split('?', maxsplit=1)[0]
        return link
