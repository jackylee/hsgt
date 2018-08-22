# -*- coding: utf-8 -*-
import scrapy
import datetime
import logging
import sys
import pymysql
from hkex.items import *

def daterange(start_date, end_date):
    if(start_date <= end_date):
        for n in range((end_date - start_date).days + 1):
            yield start_date + datetime.timedelta(n)
    else:
        for n in range((start_date - end_date).days + 1):
            yield end_date + datetime.timedelta(n)

class StocksSpider(scrapy.Spider):
    name = 'stocks'
    sz_start_url = 'http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sz'
    sh_start_url = 'http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sh'
    hk_start_url = 'http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=hk'
    sh_crawled_day = set()
    sz_crawled_day = set()
    hk_crawled_day = set()
    jobs = []
    today_str = datetime.date.today().strftime("%Y%m%d")

    def start_requests(self):
        end_date = datetime.date.today()
        conn = pymysql.connect(host = "127.0.0.1", user = "root", db = "hkex", 
            password = "", port = 3306, charset="utf8")
        cursor = conn.cursor()
        cursor.execute('select * from crawl_status where id = "1"')
        rows = cursor.fetchall()
        crawl_date = rows[0][1]
        start_date = datetime.date(year=int(crawl_date[0:4]), month=int(crawl_date[4:6]), day=int(crawl_date[6:8]))
        date_range = daterange(start_date, end_date)
        today = datetime.date.today()
        cursor = conn.cursor();
        cursor.execute('update crawl_status set crawl_date = %s where id = "1"', self.today_str)
        for day in date_range:
            self.jobs.append(day)
        self.sh_crawled_day.add(today)
        self.sz_crawled_day.add(today)
        self.hk_crawled_day.add(today)
        yield scrapy.Request(url = self.sz_start_url, callback=self.parse)
        yield scrapy.Request(url = self.sh_start_url, callback=self.parse)
        yield scrapy.Request(url = self.hk_start_url, callback=self.parse)

    def parse(self, response):
        rows = response.css('table.result-table>tr')
        sec = response.url[-2:]
        index = 0
        dates = "".join(response.css('div#pnlResult>div:first-child::text').extract()).strip().split(':')[1].split('/')
        day = dates[0].strip()
        month = dates[1].strip()
        year = dates[2].strip()
        stock_date = year + month + day
        for row in rows:
            if index == 0 or index == 1:
                index = index + 1
                continue
            #截止日期
            try:
                stock_code = "".join(row.css('td::text')[0].extract()).strip()
                stock_name = "".join(row.css('td::text')[1].extract()).strip()
                stock_hold = "".join(row.css('td::text')[2].extract()).strip().replace(',', '')
                stock_percent = "".join(row.css('td::text')[3].extract()).strip()[:-1]
                item = HkexItem()
                item['stock_code'] = stock_code
                item['stock_name'] = stock_name
                item['stock_hold'] = stock_hold
                item['stock_percent'] = stock_percent
                item['stock_date'] = stock_date
                if sec == "sh" or sec == "sz":
                    item['ishk'] = 0
                else:
                    item['ishk'] = 1
                yield item
            except:
                e = sys.exc_info()[0]
                logging.warning("parse item incorrect" + "".join(e))
                pass
            
        #print(stock + " " + percent)
        for job in self.jobs:
            if sec == "sh" and not job in self.sh_crawled_day:
                logging.warning("crawling sh" + job.strftime("%Y-%m-%d") )
                day = job.strftime("%d")
                month = job.strftime("%m")
                year = job.strftime("%Y")
                self.sh_crawled_day.add(job)
                yield scrapy.FormRequest.from_response(response, 
                    formdata={'ddlShareholdingDay': day, 'ddlShareholdingMonth': month, 'ddlShareholdingYear':year, 
                    'today': self.today_str, 'btnSearch.x': '33', 'btnSearch.y': '12'},
                    callback=self.parse)
                break
            elif sec == "sz" and not job in self.sh_crawled_day:
                logging.warning("crawling sz" + job.strftime("%Y-%m-%d"))
                day = job.strftime("%d")
                month = job.strftime("%m")
                year = job.strftime("%Y")
                self.sz_crawled_day.add(job)
                yield scrapy.FormRequest.from_response(response, 
                    formdata={'ddlShareholdingDay': day, 'ddlShareholdingMonth': month, 'ddlShareholdingYear':year, 
                    'today': self.today_str, 'btnSearch.x': '33', 'btnSearch.y': '12'},
                    callback=self.parse)
                break
            elif sec == 'hk' and not job in self.hk_crawled_day:
                logging.warning("crawling hk" + job.strftime("%Y-%m-%d"))
                day = job.strftime("%d")
                month = job.strftime("%m")
                year = job.strftime("%Y")
                self.hk_crawled_day.add(job)
                yield scrapy.FormRequest.from_response(response, 
                    formdata={'ddlShareholdingDay': day, 'ddlShareholdingMonth': month, 'ddlShareholdingYear':year, 
                    'today': self.today_str, 'btnSearch.x': '33', 'btnSearch.y': '12'},
                    callback=self.parse)
                break
