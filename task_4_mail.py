from lxml import html
import requests
from pprint import pprint

from pymongo import MongoClient

url = 'https://news.mail.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/92.0.4515.159 Safari/537.36'}

response = requests.get(url, headers=headers)

dom = html.fromstring(response.text)

items = dom.xpath("//div[contains(@class, 'cols__column ')]")
list_items = []

for item in items:
    item_info = {}
    title_group_newss = item.xpath(".//span[@class='hdr__inner']/text()")
    news_title = item.xpath(".//span[@class='newsitem__title-inner']/text()")
    link_news = item.xpath(".//a[contains(@class, 'newsitem__title link-holder')]/@href")
    news_source = item.xpath(".//span[@class='newsitem__param']/text()")
    time_news = item.xpath(".//span[contains(@class, 'newsitem__param')]/@datetime")
    info = item.xpath(".//span[contains(@class,'newsitem__text')]/text()")
    list_mini_items = item.xpath(".//li[@class='list__item']")

    item_info['title_group_newss'] = title_group_newss[0]
    item_info['news_title'] = news_title[0]
    item_info['link_news'] = link_news[0]
    item_info['news_source'] = news_source[0]
    item_info['time_news'] = time_news[0]
    item_info['info'] = info[0].replace('\xa0', ' ')

    list_items.append(item_info)

    for item_mini in list_mini_items:
        item_info = {}
        item_info['title_group_newss'] = title_group_newss[0]
        news_title = item_mini.xpath(".//span[@class='link__text']/text()")
        link_news = item_mini.xpath(".//a[contains(@class, 'link')]/@href")
        response = requests.get(link_news[0], headers=headers)
        dom_mini = html.fromstring(response.text)
        news_source = dom_mini.xpath("//div[contains(@class, 'breadcrumbs')]//span[@class='link__text']/text()")
        time_news = dom_mini.xpath("//div[contains(@class, 'breadcrumbs')]//@datetime")
        info = item_mini.xpath(".//span[@class='link__text']/text()")

        item_info['news_title'] = news_title[0]
        item_info['link_news'] = link_news[0]
        item_info['news_source'] = news_source[0]
        item_info['time_news'] = time_news[0]
        item_info['info'] = info[0].replace('\xa0', ' ')

        list_items.append(item_info)

# -------------------------------------------------------------------------------------------------
# Подключаем БД
client = MongoClient('127.0.0.1', 27017)
db = client['news_day']

news = db.news

for el in list_items:
    news.insert_one({
        "title_group_newss": el['title_group_newss'],
        "news_title": el['news_title'],
        "link_news": el['link_news'],
        "news_source": el['news_source'],
        "time_news": el['time_news'],
        "info": el['info'],
    })


pprint(list_items)
print(len(list_items))
