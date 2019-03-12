# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import redis
import urllib
import json


class TmallDetailSpider(scrapy.Spider):
    name = 'tmall_detail_spider'
    allowed_domains = ['list.tmall.com', 'detail.m.tmall.com', 'detail.tmall.com', 'tmall.com']
    start_urls = [
        'https://mdetail.tmall.com/mobile/itemPackage.do?'
    ]


    def __init__(self):
        super(TmallDetailSpider, self).__init__()
        self.db_index = {
            'tmall_detail': 15,  # 商品详情地址数据库
            'tmall_rate': 14,  # 商品评论地址数据库
        }
        self.redis_db = redis.Redis(host="localhost", port=6379, db=self.db_index['tmall_detail'])
        self.create_url()
        self.rate_num = 0
        pass

    def get_itemID(self):
        ID = eval(self.redis_db.lpop('tmall_detail_id'))['item_id']
        return ID

    """生成要爬取的URL"""
    def create_url(self):
        self.detail_api = {
            'itemId': self.get_itemID()  # 商品的ID
            # 'sellerId': 1652528654,  # 商家的ID
            # 'currentPage': 1,
            # 'pageSize': '10'
        }
        url = 'https://mdetail.tmall.com/mobile/itemPackage.do?' + urllib.urlencode(self.detail_api)
        return url

    def parse(self, response):
        # jsessionid = re.findall('JSESSIONID=(.*?);', str(response.headers.getlist('Set-Cookie')))[0]
        # self.set_cookie(jsessionid)
        # yield Request(self.create_url(), callback=self.parse_rate)
        for i in range(0, 10000):
            yield Request(self.create_url(), callback=self.parse_rate, dont_filter=True)
        pass

    def parse_rate(self, response):
        # body = json.loads(response.body)
        body = json.loads(response.body_as_unicode())
        yield body
        self.rate_num += 1
        print "当前爬取了", self.rate_num, "条商品的详情信息"
        pass
