# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BoketeCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    odai_id = scrapy.Field()
    odai_image = scrapy.Field()
