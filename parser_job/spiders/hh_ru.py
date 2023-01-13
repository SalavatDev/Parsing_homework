import scrapy
from scrapy.http import HtmlResponse
from parser_job.items import ParserJobItem


def pars_salary(list_in):
    res = []
    for i in range(len(list_in)):
        if list_in[i].find('от') != -1:
            if i + 1 != len(list_in):
                res.append({'от': list_in[i + 1].replace('\xa0', '')})
        elif list_in[i].find('до') != -1:
            if i + 1 != len(list_in):
                res.append({'до': list_in[i + 1].replace('\xa0', '')})
        elif list_in[i].find('USD') != -1:
            res.append({'валюта': 'USD'})
        elif list_in[i].find('руб') != -1:
            res.append({'валюта': 'руб.'})
        elif list_in[i].find('на руки') != -1:
            res.append('на руки')

    return res


class HhRuSpider(scrapy.Spider):
    name = 'hh_ru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://kazan.hh.ru/search/vacancy?text=C%2B%2B&from=suggest_post&area=88']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

        urls_vacancies = response.xpath("//div[@class='vacancy-serp-item-body__main-info']//a[@data-qa='serp-item__title']/@href").getall()
        for url_vacancy in urls_vacancies:
            yield response.follow(url_vacancy, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        vacancy_name = response.css("h1::text").get()
        vacancy_salary = response.xpath("//span[@data-qa='vacancy-salary-compensation-type-net']//text()").getall()
        salary = pars_salary(vacancy_salary)

        vacancy_url = response.url

        yield ParserJobItem(
            name=vacancy_name,
            salary=salary,
            url=vacancy_url
        )
