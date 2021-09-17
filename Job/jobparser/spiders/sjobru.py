import scrapy
from scrapy.http import HtmlResponse
from  Job.jobparser.items import JobparserItem


class SjobruSpider(scrapy.Spider):
    name = 'sjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Bt%5D%5B0%5D=4',
                  'https://spb.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response: HtmlResponse):
        urls = response.xpath("//div[contains(@class,'f-test-vacancy-item ')]//a[@target='_blank']/@href").getall()
        next_page = response.xpath("//a[contains(@class,'f-test-button-dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for url in urls:
            yield response.follow(url, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        adress = response.xpath("//div[contains(@class,'f-test-address')]/span/span//text()").getall()
        salary = response.xpath("//div[contains(@class, 'f-test-vacancy-base-info')]/div[2]/div/div/div/span/span//text()").getall()
        vac_info = response.xpath("//div[contains(@class,'f-test-vacancy-base-info')]/div[2]/span//text()").getall()
        url = response.url
        item = JobparserItem(name=name, adress=adress, vac_info=vac_info, salary=salary, url=url)
        yield item
