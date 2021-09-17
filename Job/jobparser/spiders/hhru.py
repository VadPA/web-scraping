import scrapy
from scrapy.http import HtmlResponse
from Job.jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://tambov.hh.ru/search/vacancy?fromSearchLine=true&st=searchVacancy&text=Python&from=suggest_post&area=1',
        'https://tambov.hh.ru/search/vacancy?fromSearchLine=true&st=searchVacancy&text=Python&from=suggest_post&area=2',
        'https://tambov.hh.ru/search/vacancy?fromSearchLine=true&st=searchVacancy&text=Python&from=suggest_post&area=3']

    def parse(self, response: HtmlResponse):
        urls = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for url in urls:
            yield response.follow(url, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1//text()").get()
        adress = response.xpath("//p[@data-qa='vacancy-view-location']/text()").getall()
        vac_info = response.xpath("//div[@data-qa='vacancy-description']//ul//text()").getall()
        salary = response.css("p.vacancy-salary span::text").get().replace('\xa0', '')
        url = response.url
        item = JobparserItem(name=name, adress=adress, vac_info=vac_info, salary=salary, url=url)
        yield item
