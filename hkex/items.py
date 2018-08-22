# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HkexItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    stock_code = scrapy.Field()
    stock_name = scrapy.Field()
    stock_hold = scrapy.Field()
    stock_percent = scrapy.Field()
    stock_date = scrapy.Field()
    ishk = scrapy.Field()
    pass
