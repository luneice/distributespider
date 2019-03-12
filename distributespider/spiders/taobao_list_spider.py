# --*coding=utf-8*--
import scrapy
import json
from scrapy.http import Request
import random
import urllib


class TaobaoSpider(scrapy.Spider):
    name = 'taobao_list_spider'

    def __init__(self):
        super(TaobaoSpider, self).__init__()
        self.search_item_api = {
            "pape": 1,
            "q": '',
            "n": "20",
            "style": "list",
            "sst": "1",
            "buying": "buyitnow"
        }
        self.change_keywords()
        pass

    def create_url(self):
        url = "https://s.m.taobao.com/search?"
        url += urllib.urlencode(self.search_item_api)
        return url

    def next_page(self):
        self.search_item_api["pape"] += 1
        pass

    def change_keywords(self):
        list = {
            "1": "平板电脑",
            "2": "平板电脑",
            "3": "平板电脑",
            "4": "平板电脑",
            "5": "平板电脑",
            "6": "平板电脑",
            "7": "平板电脑",
            "8": "平板电脑",
            "9": "平板电脑",
            "10":"平板电脑"
        }
        self.search_item_api['q'] = list[str(random.randint(1,10))]
        pass

    def start_requests(self):
        for i in range(0,10000):
            yield Request(url=self.create_url(), method='GET', callback=self.parse)
            self.next_page()
        pass

    def parse(self, response):
        body = json.loads(response.body_as_unicode())
        if body['itemsArray']:
            for item in body['itemsArray']:
                item["merchandise"]=self.search_item_api['q']
                yield item
        pass
