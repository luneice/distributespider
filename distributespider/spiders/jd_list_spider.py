# -*- coding: utf-8 -*-
import scrapy
import redis
from scrapy.http import *
from mobile_ua_list import USER_AGENTS
from distributespider.items import JdspiderItem
import time
import random
import json
import distributespider.custom_settings as settings


class JdListSpiderSpider(scrapy.Spider):
    name = "jd_list_spider"
    allowed_domains = ["jd.com", "so.m.jd.com"]
    start_urls = []

    """调试过程中临时cookies"""
    cookies = "_med=dw:1366&dh:768&pw:1366&ph:768&ist:0; pnm_cku822=019UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FSn5Fe097RHxEeS8%3D%7CU2xMHDJ7G2AHYg8hAS8XIw0tA0UkQj5PYTdh%7CVGhXd1llXGhdaVJsWGxTa1NuWWRGeEJ6Rn5Kdkp0QHVJcUl1TXVbDQ%3D%3D%7CVWldfS0SMg03FysUNBokSXxVaFZrUHpOdFF%2FKX8%3D%7CVmhIGCcbOwYmGiQcIAA4DTQMLBAuFS4ONA86GiYYIxg4AjsBVwE%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; cq=ccp%3D1; t=5159478f459446f5afa77f55adadfea7; cookie2=19d1002391c09daaa4a447b2461f1dea; _tb_token_=1bc7ecab581f; _m_h5_tk=3ebf1efc9d0c27b5693625859d7ce2a4_1499425022688; _m_h5_tk_enc=4d8050cdf5488121fdea248e6d620e5d; cna=l8fcET2/bRECAT24S9eWeWeV; l=AoWF9TwOdmBO18rvmvVos2UfFdq/QDlD; isg=And3GmR94hFLkWaVMsY80EBHBmJTsEue4qeifckkkcY6eJW60Q2A7pYaIGLZ"

    """定义请求头"""
    HEADERS = {
        ':authority': 'so.m.jd.com',
        ':method': 'POST',
        ':path': '/ware/searchList.action',
        ':scheme': 'https',
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.8',
        'cache-control': 'no-cache',
        'content-length': '42',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': cookies,
        'dnt': '1',
        'origin': 'https://so.m.jd.com',
        'pragma': 'no-cache',
        'referer': 'https://so.m.jd.com/ware/search.action?keyword=%E7%99%BD%E9%85%92',
        'user-agent': random.choice(USER_AGENTS),
        'x-requested-with': 'XMLHttpRequest',
    }


    """spider的构造函数"""
    def __init__(self, category=None, *args, **kwargs):
        super(JdListSpiderSpider, self).__init__(*args, **kwargs)
        # 获取Redis的配置参数
        self.db_index = settings.redis_index
        # 连接到Redis数据库cookies池
        self.redis_db = redis.Redis(host="localhost", port=6379, db=self.db_index['cookies'])
        # 构造爬虫的访问接口
        self.search_item_api = {
            '_format_': 'json',
            'sort': '',
            'page': '0',
            'keyword': '手机'
        }
        self.error = 0
        self.crawl_num = 0
        self.goods_num = 0
        self.change_keywords("平板电脑")
        self.start_urls.append(self.create_url())
        pass

    """请求参数的处理"""
    def create_url(self):
        url = 'https://so.m.jd.com/ware/searchList.action'
        return url

    """下一页"""
    def next_page(self, page):
        self.search_item_api['page'] = str(page)
        pass

    """更换查询的关键词"""
    def change_keywords(self, keywords):
        self.search_item_api['keyword'] = keywords
        pass

    """"spider默认的回调函数"""
    def parse(self, response):
        start = time.time()
        """循环地爬取仅爬取"""
        for i in range(0, 1000):
            self.next_page(i)
            i += 1
            meta = {'request_ok': i}  # 作为代理是否成功的标志
            yield FormRequest(self.create_url(), formdata=self.search_item_api,
                              method='POST', callback=self.parse_item, meta={'request_ok': i})
        end = time.time()
        during = end - start
        print '耗时', during
        pass

    """处理接口返回的结果"""
    def parse_item(self, response):
        try:
            item = JdspiderItem()
            jsondata = json.loads(response.body)
            wareList_data = json.loads(jsondata['value'])
            wareList = wareList_data['wareList']
            wareList = wareList['wareList']
            lenght = len(wareList)
            self.crawl_num += 1
            self.goods_num += lenght
            print "当前爬取了", self.crawl_num, "个页面\t", \
                "当前页面有", lenght, "条信息\t", \
                "当前爬取了", self.goods_num, "条商品信息"
            # print "当前页面有", lenght, "条信息"
            # print "当前爬取了", self.goods_num, "条商品信息"
            for i in range(0, lenght):
                item['jd_data'] = wareList[i]
                yield item
        except:
            self.error += 1
            print '请求接口的数据出错', self.error
            jsondata = json.loads(response.body)
            print jsondata
            return
        pass

    """请求头的处理"""
    def set_headers(self):
        # 从redis中获取cookies
        self.redis_db.execute_command('select\b' + str(self.db_index['cookies']))
        cookies = self.redis_db.lpop("cookies")
        # 设置请求头的cookies
        self.HEADERS['cookie'] = cookies
        pass
