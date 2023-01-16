import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from lrm_parser.items import LrmParserItem


class LeroymerlinRuSpider(scrapy.Spider):
    name = 'leroymerlin_ru'
    allowed_domains = ['castorama.ru']
    start_urls = ['https://www.castorama.ru/catalogsearch/result/?q=%D0%BA%D0%B2%D0%B0%D1%80%D1%86%D0%B2%D0%B8%D0%BD%D0%B8%D0%BB%D0%BE%D0%B2%D1%8B%D0%B9%20%D0%BB%D0%B0%D0%BC%D0%B8%D0%BD%D0%B0%D1%82']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@class='product-card__img-link']/@href")
        for link in links:
            yield response.follow(link, callback=self.parse_orders)

    def parse_orders(self, response: HtmlResponse):
        print()
        # name = response.xpath("//h1/text()").get()
        # price = response.xpath("//span[@class='price']/span/span/text()").getall()
        # photos = response.xpath("//ul[@class='swiper-wrapper']/li/img/@src").getall()
        # url = response.url
        # yield LrmParserItem(name=name, price=price, photos=photos, url=url)
        loader = ItemLoader(item=LrmParserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//span[@class='price']/span/span/text()")
        loader.add_xpath('photos', "//ul[@class='swiper-wrapper']/li/img/@src")
        loader.add_value('url', response.url)
        yield loader.load_item()


