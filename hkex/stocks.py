#!/usr/bin/env python
#coding=utf-8
import json
import scrapy
import codecs
import sys

class HkexItem(scrapy.Item):
    stock_name = scrapy.Field()
    stock_code = scrapy.Field()
    stock_hold = scrapy.Field()
    stock_percent = scrapy.Field()
    stock_date = scrapy.Field()

def unicode_tranform(unicode_str):
    cc = str(unicode_str).decode('unicode_escape')
    ccc = cc.encode('utf-8')
    return ccc
def stock_stat():
    handle = codecs.open('stock.json', encoding="utf-8")
    data = []
    stock_dict = {}
    for line in handle:
        data.append(json.loads(line))

    index = 0
    for d in data:
        try:
            stock_code = str(d['stock_code'])
            stock_name = d['stock_name']
            print(stock_code + stock_name)
            if index == 10:
                break
            index = index + 1
        except Exception as e:
            pass
        
if __name__ == "__main__":
    stock_stat()
