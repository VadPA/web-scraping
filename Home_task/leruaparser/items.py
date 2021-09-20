# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def get_price(value):
    try:
        value = int(value.replace('\xa0', ''))
    except Exception:
        return value
    return value


class LeruaparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # name = scrapy.Field(output_processor=TakeFirst())
    # price = scrapy.Field(input_processor=MapCompose(get_price), output_processor=TakeFirst())
    # currency = scrapy.Field(output_processor=TakeFirst())
    # unit = scrapy.Field(output_processor=TakeFirst())
    # info = scrapy.Field(output_processor=TakeFirst())
    # photos = scrapy.Field()
    # url = scrapy.Field()

    name = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    unit = scrapy.Field()
    info = scrapy.Field()
    photos = scrapy.Field()
    spec = scrapy.Field()
    spec_values = scrapy.Field()
    spec_prod = scrapy.Field()
    url = scrapy.Field()
    _id = scrapy.Field()
