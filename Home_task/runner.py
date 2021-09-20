from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from API.Lesson_7.Home_task.leruaparser.spiders.leruaru import LeruaruSpider
from API.Lesson_7.Home_task.leruaparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeruaruSpider, query='доска')

    process.start()




