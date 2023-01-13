import scrapy
from scrapy.http import HtmlResponse
from parser_job.items import ParserJobItem


class SuperjobRuSpider(scrapy.Spider):
    name = 'superjob_ru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=C%2B%2B%20developer']

    def parse(self, response):
        next_page = response.xpath(
            "//a[@class='_1IHWd _6Nb0L _37aW8 _3BLGT f-test-button-dalshe f-test-link-Dalshe']/@href").get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

        urls_vacancies = response.xpath(
            "//span[@class='_2KHVB _3l13l _3l6qV _3PTah _3xCPT rygxv _17lam _2Ovds']//a//@href").getall()
        for url_vacancy in urls_vacancies:
            yield response.follow(url_vacancy, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        vacancy_name = response.css("h1::text").get()
        vacancy_salary = response.xpath("//span[@class='_2eYAG _3xCPT rygxv _3GtUQ']//text()").getall()
        #salary = pars_salary(vacancy_salary)

        vacancy_url = response.url

        yield ParserJobItem(
            name=vacancy_name,
            salary=vacancy_salary,
            url=vacancy_url
        )
