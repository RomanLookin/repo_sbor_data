# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from bs4 import BeautifulSoup
import requests

class SJruSpider2(scrapy.Spider):
    name = 'sjru2'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vakansii/programmist-python.html?geo%5Bt%5D%5B0%5D=4']
    tot=1

    def parse(self, response: HtmlResponse):  #
        next_page = 'https://superjob.ru' \
            + response.css('a[class="icMQ_ bs_sM _3ze9n _3RBrN f-test-button-dalshe f-test-link-Dalshe"]').attrib['href']  #
        print(next_page)
        response.follow(next_page, callback=self.parse)

        #vacansy = response.css(
        #    #'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header '
        #    #'a.bloko-link::attr(href)'
        #).extract()
        #https://superjob.ru' +
        vacansy=response.xpath('//div[@class="_1U0tH _2aBG1 vnBET"]/a/@href').extract()
        #print(vacansy)

        for link in vacansy:
            yield response.follow('https://superjob.ru'+link, callback=self.vacansy_parse)

        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)


    def vacansy_parse(self, response: HtmlResponse):

        #name = response.css('h1[data-qa="vacancy-title"]::text').getall()
        name=response.css('h1[class="rFbjy _25mwC _2aBG1 _2q8ij"]::text').getall()
        #salary = ''.join(response.css('span[data-qa="vacancy-serp__vacancy-compensation"]'
        #                              '[class="bloko-header-section-3 bloko-header-section-3_lite"]::text').getall())
        #sal1=response.css('span[class="_2Wp8I _1U0tH _2aBG1"]::text').getall()
        #sal2=response.css('span[class="_1U0tH _2aBG1"]::text').getall()
        #salary=sal1+sal2 #''.join()
        #                    [class=""]

        qusp = response.xpath('//span[@class="_1OuF_ ZON4b"]/descendant::node()/text()').extract()
        salary=''.join(qusp)
        print(str(self.tot)+' Название вакансии: ', name[0])
        print('Зарплата: ', salary)

        self.tot=self.tot+1

        yield JobparserItem(name=name, salary=salary)