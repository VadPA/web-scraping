# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class LeruaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.products2009

    def process_item(self, item, spider):
        item['spec_values'] = [el.replace('\n                ', '').rstrip() for el in item['spec_values']]
        item['spec_values'] = [el.replace('\n            ', '').lstrip() for el in item['spec_values']]
        item['spec_prod'] = self.process_spec(item['spec'], item['spec_values'])
        item['price'] = float(item['price'])
        del item['spec']
        del item['spec_values']
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

    def process_spec(self, spec, spec_value):
        specification = {}
        for i, el in enumerate(spec):
            specification[el] = spec_value[i]
        return specification



class LeruaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)


    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
