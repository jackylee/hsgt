# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import pymysql
import scrapy

#class HkexPipeline(object):
#    def __init__(self):
#        self.file = codecs.open('stock.json', 'wb')
#    def process_item(self, item, spider):
#         line = json.dumps(dict(item), ) + "\n"
#         self.file.write(line.encode("utf-8"))
#
#    def close_spider(self, spider):
#        self.file.close()

class MysqlPipeline(object):
    def open_spider(self, spider):
        self.conn = pymysql.connect(host = "127.0.0.1", user = "root", db = "hkex", 
            password = "", port = 3306, charset="utf8")
        self.cursor = self.conn.cursor()
    
    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        self.cursor.execute("""insert into stock_data(stock_code, stock_name, stock_hold, stock_percent, stock_date) values(%s, %s, %s, %s, %s)""", ( item['stock_code'], item['stock_name'], item['stock_hold'], item['stock_percent'], item['stock_date']))
        self.conn.commit()

