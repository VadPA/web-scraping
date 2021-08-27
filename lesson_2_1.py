from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['library']
# db2 = client['auto']

human = db.human
# books = db.books


