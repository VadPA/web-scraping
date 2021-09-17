# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPipeline:
        def __init__(self):
            client = MongoClient('localhost', 27017)
            self.mongobase = client.vacancies1709

        def process_item(self, item, spider):
            item['vac_info'] = [el for el in item['vac_info'] if el != ' ']
            item['adress'] = "".join([el for el in item['adress'] if el != ', '])
            (s1, s2, s3, s4) = self.process_salary_hh(item['salary']) if spider.name != 'sjobru' else self.process_salary_sjob(item['salary'])
            item['salary_min'], item['salary_max'], item['salary_cur'], item['salary_period'] = (s1, s2, s3, s4)
            if spider.name == 'sjobru':
                item['salary'] = " ".join(
                    [el.replace('\xa0', ' ') for el in item['salary'] if (el != '') & (el != '\xa0')])
            else:
                item['salary'] = "".join(
                    [el.replace('\xa0', ' ') for el in item['salary'] if (el != '') & (el != '\xa0')])
            collection = self.mongobase[spider.name]
            collection.insert_one(item)
            return item

        def process_salary_sjob(self, salary):
            if ('з/п не указана' in salary) | ('По договорённости' in salary) | (len(salary) == 0):
                salary_min = None
                salary_max = None
                salary_cur = None
                salary_period = None
                return salary_min, salary_max, salary_cur, salary_period
            list_salary = [el.replace('\xa0', ' ') for el in salary if (el != '') & (el != '\xa0') & (el != '/')]
            if ('день' in list_salary) | ('месяц' in list_salary):
                salary_period = list_salary[-1]
                del list_salary[-1]
            else:
                salary_period = None
            str_salary = " ".join(list_salary)
            list_salary = str_salary.split(' ')
            salary_cur = list_salary[-1].replace(".", '')
            del list_salary[-1]
            if ('от' in list_salary) & ('до' in list_salary):
                salary_min = int(list_salary[1] + list_salary[2])
                salary_max = int(list_salary[3] + list_salary[4])
            elif len(list_salary) == 3:
                if list_salary[0] == 'от':
                    salary_min = int(list_salary[1] + list_salary[2])
                    salary_max = None
                elif list_salary[0] == 'до':
                    salary_min = None
                    salary_max = int(list_salary[1] + list_salary[2])
                else:
                    salary_min = int(list_salary[0])
                    salary_max = int(list_salary[1])
            elif (len(list_salary) == 4):
                salary_min = int(list_salary[0] + list_salary[1])
                salary_max = int(list_salary[2] + list_salary[3])
            elif (len(list_salary) == 5) & (chr(8212) in list_salary):
                salary_min = int(list_salary[0] + list_salary[1])
                salary_max = int(list_salary[3] + list_salary[4])
            elif (len(list_salary) == 2):
                salary_min = int(list_salary[0] + list_salary[1])
                salary_max = None
            return salary_min, salary_max, salary_cur, salary_period

        def process_salary_hh(self, salary):
            s = salary.split(' ')
            if salary == 'з/п не указана':
                salary_min = None
                salary_max = None
                salary_cur = None
                salary_period = None
            elif len(s) == 5:
                salary_min = s[1]
                salary_max = s[3]
                salary_cur = s[4].replace('.', '')
                salary_period = 'месяц'
            elif len(s) == 3:
                if s[0] == 'от':
                    salary_min = s[1]
                    salary_max = None
                    salary_cur = s[2].replace('.', '')
                    salary_period = 'месяц'
                elif s[0] == 'до':
                    salary_min = None
                    salary_max = s[1]
                    salary_cur = s[2].replace('.', '')
                    salary_period = 'месяц'
            return salary_min, salary_max, salary_cur, salary_period
