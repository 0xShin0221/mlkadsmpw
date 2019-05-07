# -*- coding: utf-8 -*-
import scrapy
import json
from time import sleep
from bokete_crawler.items import BoketeCrawlerItem

from scrapy.selector import Selector
from scrapy.http import Request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class BoketeSpider(scrapy.Spider):
    name = 'bokete'
    allowed_domains = ['bokete.jp']
    start_urls = ['https://bokete.jp/']

    def __init__(self, page_limit=5):
        #self.search_word = search_word
        self.page_limit = int(page_limit)

    def start_requests(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://bokete.jp/odai/popular?page=1')

        #現状forbidenなし|Avoid getting banned
        sel = Selector(text=self.driver.page_source)
        forbidden_page_title = sel.xpath('//title/text()').extract_first()
        if '403' in forbidden_page_title:
            self.logger.warn('Access is forbidden. Try again!')
            # input_search_form2 = self.driver.find_element_by_xpath(
            #     '//input[@name="search_block_form"]')
            # input_search_form2.send_keys(self.search_word)
            # input_search_form2.send_keys(Keys.RETURN)

        page_num = 1

        while page_num < self.page_limit:
            try:
                print("今何ページ",page_num)
                odai_arrays = []
                sel = Selector(text=self.driver.page_source)
                odai_urls = sel.xpath('//article/div/h3/a/@href').extract()
                for i in range(1,10):
                    #SearchSelector
                    sel = Selector(text=self.driver.page_source)
                    odai_urls = sel.xpath("//*[@id='content']/div[2]/div[{}]/div/h3/b/a".format(i))
                    for j in odai_urls:
                        odai_link = j.xpath('@href').extract()[0]
                        odai_url = "https://bokete.jp" + odai_link
                        yield Request(url=odai_url, callback=self.parse_item)

                # Process a next page
                page_num = page_num + 1
                current_url = self.driver.current_url
                next_url = current_url[:-1] + str(page_num)
                print("次のurl",next_url)
                next_page = self.driver.get(next_url)

                sleep(2)
            except NoSuchElementException:
                self.driver.quit()
        else:
            self.driver.quit()

    def parse_item(self, response):
        sleep(1)

        odai_ids = response.xpath('//*[@id="content"]/div[1]/div[1]/div/div/a')
        for i in odai_ids:
            bokete_item = BoketeCrawlerItem()
            bokete_item['odai_id'] = i.xpath('@href').extract()[0]
            bokete_item['odai_image'] = response.xpath('//*[@id="content"]/div[1]/div[1]/div/div/a/img/@src').extract()[0]
        yield bokete_item
        #
        # response = json.loads(response.body)
        # result = response['response']['odai'][0]
        #
