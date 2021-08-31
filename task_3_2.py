from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']

vacancy = db.vacancy

wages = int(input('Введите необходимый размер оплаты труда: '))

dict_temp = [el for el in vacancy.find({'$or': [{'salary_min': {'$gte': wages}}, {'salary_max': {'$gte': wages}}]})]
pprint(dict_temp)
