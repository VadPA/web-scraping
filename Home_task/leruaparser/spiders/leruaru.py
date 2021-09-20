import scrapy
from scrapy.http import HtmlResponse
from API.Lesson_7.Home_task.leruaparser.items import LeruaparserItem
from scrapy.loader import ItemLoader


class LeruaruSpider(scrapy.Spider):
    name = 'leruaru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query):
        super(LeruaruSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}']


    def parse(self, response: HtmlResponse, **kwargs):
        products_links = response.xpath("//a[@data-qa='product-name']")
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for link in products_links:
            yield response.follow(link, callback=self.parse_products)


    def parse_products(self, response: HtmlResponse):
        # loader = ItemLoader(item=LeruaparserItem(), response=response)
        # loader.add_xpath('name', "//h1/text()")
        # loader.add_xpath('price', "//span[@slot='price']/text()")
        # loader.add_xpath('currency', "//span[@slot='currency']/text()")
        # loader.add_xpath('unit', "//span[@slot='unit']/text()")
        # loader.add_xpath('info', "//div/p/text()")
        # loader.add_xpath('photos', "//picture[@slot='pictures']/img/@src")
        # loader.add_value('url', response.url)
        # yield loader.load_item()

        # name = response.xpath("//a[contains(@data-qa, 'product-image')]/@aria-label").get()
        # price = response.xpath("//div[contains(@data-qa, 'product-primary-price')]/p/text()").get()
        # photos = response.xpath("//a[contains(@data-qa, 'product-image')]//picture").get()
        name = response.xpath("//h1/text()").get()
        price = response.xpath("//span[@slot='price']/text()").get()
        currency = response.xpath("//span[@slot='currency']/text()").get()
        unit = response.xpath("//span[@slot='unit']/text()").get()
        info = response.xpath("//div/p/text()").getall()
        spec = response.xpath("//dl/div/dt[@class='def-list__term']/text()").getall()
        spec_values = response.xpath("//dl/div/dd[@class='def-list__definition']/text()").getall()
        photos = response.xpath("//picture[@slot='pictures']/img/@src").getall()
        url = response.url
        yield LeruaparserItem(name=name, price=price, currency=currency, info=info, unit=unit, photos=photos, spec=spec, spec_values=spec_values, url=url)


