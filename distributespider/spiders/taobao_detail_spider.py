# -*- coding: utf-8 -*-
import scrapy
import redis
from scrapy.http import Request
import json
import re


class TaobaoDetail(scrapy.Spider):
    name = 'taobao_detail_spider'

    def __init__(self):
        super(TaobaoDetail, self).__init__()
        self.db = redis.Redis('localhost', 6379, 0)
        self.rate_num = 0
        pass

    def create_url(self):
        url = "https://mdetail.tmall.com/mobile/itemPackage.do?itemId="
        url += self.getItemid()
        return url

    def getItemid(self):
        ID = self.db.lpop('Item_id')
        return ID

    def start_requests(self):
        url = self.create_url()
        yield Request(url = url, callback=self.parse, method="POST")
        pass

    def parse(self, response):
        for i in range(0, 1000):
            yield Request(url = self.create_url(), callback=self.parse_item, dont_filter=True)
        pass

    def parse_item(self, response):
        body = json.loads(response.body_as_unicode())
        self.item = dict(body['model'])
        self.item['item_id'] = re.search('itemId=(.*)', response.url).group(1)
        yield self.item
        self.rate_num += 1
        print "当前爬取了", self.rate_num, "条商品详情信息"
        pass