from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from Job.jobparser import settings
from Job.jobparser.spiders.sjobru import SjobruSpider
from Job.jobparser.spiders.hhru import HhruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(crawler_settings)
    process.crawl(SjobruSpider)
    process.crawl(HhruSpider)

    process.start()


