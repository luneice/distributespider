# -*- coding: utf-8 -*-
import scrapy
import redis
import urllib
from distributespider.items import TmallspiderItem as tmall_dic
from scrapy.spiders import Request
import time
import re
import random
from mobile_ua_list import USER_AGENTS


class TmallListSpider(scrapy.Spider):
    name = 'tmall_list_spider'
    allowed_domains = ['tmall.com']
    start_urls = ['https://soft.luneice.com']

    """调试过程中临时cookies"""
    cookies = "cookie2=1cde766075c6bd692962767d8e67afda; t=e883170067fe79e3f31d02eec21b3dbe; _tb_token_=fb7ebdd0ba38e; _m_h5_tk=9f531a7f03eb684fcdb6f11d3863e882_1498372014428; _m_h5_tk_enc=8f89e2fff6a593fa96d0ff017e524c5a; cna=9TbWEaXIfn4CAT24S9ffHlyS; isg=Avb2HYabsw72W0fq2LcPhQwZRyXyGjJJS-wD2mDf4ll0o5Y9yKeKYVxRw0Uw"

    """定义请求头"""
    HEADERS = {
        # ':authority': 'list.tmall.com',
        # ':method': 'GET',
        # ':path': '/m/search_items.htm?page_size=20&page_no=4&q=%BF%DA%BA%EC&type=p&'
        #          'tmhkh5=&spm=a223j.8443192.a2227oh.d100&from=mallfp..m_1.13_hq',
        # ':scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'zh-CN,zh;q=0.8',
        'cache-control': 'no-cache',
        'cookie': cookies,
        'pragma': 'no-cache',
        'connection': 'keep-alive',
        'referer': 'https://www.tmall.com/',
        'user-agent': random.choice(USER_AGENTS)
    }

    """
    请求的地址
    https://list.tmall.com/m/search_items.htm?page_size=20&page_no=3&q=%BF%DA%BA%EC&type=p&tmhkh5=&spm=a223j.8443192.a2227oh.d100&from=mallfp..m_1.13_hq
    """

    """spider的构造函数"""
    def __init__(self, category=None, *args, **kwargs):
        super(TmallListSpider, self).__init__(*args, **kwargs)
        self.db_index = {
            'query': 0,  # 关键词数据库
            'cookies': 1,  # cookies数据库
            'itemID,sellerID': 2
        }
        self.redis_db = redis.Redis(host="localhost", port=6379, db=self.db_index['cookies'])
        # 构造访问接口
        self.search_item_api = {
            'page_size': '20',
            'page_no': 1,  # 实现翻页功能
            'q': '',  # 查询的关键词
            'type': 'p',
            'tmhkh5': '',
            'spm': 'a223j.8443192.a2227oh.d100',
            'from': 'mallfp..m_1.13_hq'
        }
        self.change_keywords("平板电脑")
        self.crawl_num = 0
        self.goods_num = 0
        self.start_urls.append(self.create_url())
        pass

    """请求参数的处理"""
    def create_url(self):
        url = 'https://list.tmall.com/m/search_items.htm?'
        url += urllib.urlencode(self.search_item_api)
        return url

    """下一页"""
    def next_page(self):
        self.search_item_api['page_no'] += 1
        pass

    """更换查询的关键词"""
    def change_keywords(self, keywords):
        self.search_item_api['q'] = keywords  # 将关键词转换成utf8编码
        pass

    """请求头的处理"""
    def set_headers(self):
        # 从redis中获取cookies
        self.redis_db.execute_command('select\b' + str(self.db_index['cookies']))
        cookies = self.redis_db.lpop("cookies")
        # 设置请求头的cookies
        self.HEADERS['cookie'] = cookies
        pass

    """"spider默认的回调函数"""
    def parse(self, response):
        print time.asctime()
        print time.time()
        print "执行前"
        # yield Request(self.create_url(), callback=self.parse_item, headers=self.HEADERS)
        time.sleep(2)
        print "执行后"
        print time.time()
        print time.asctime()
        """循环地爬取仅爬取前一百页"""
        for i in range(0, 1000):
            self.next_page()
            time.sleep(0.01)
            # yield Request(self.create_url(), callback=self.parse_item, headers=self.HEADERS)
            self.crawl_num += 1
            for unit in range(0, 20):
                self.goods_num += 1
            print "当前爬取了", self.crawl_num, "个页面\t", \
                "当前爬取了", self.goods_num, "条商品信息"
        print time.time()
        print time.asctime()
        pass

    """处理接口返回的结果"""
    def parse_item(self, response):
        item = tmall_dic()
        """正则表达式提取接口中的item"""
        string_before = re.findall('"item":\[(.*?)\],"itemList"', response.body)
        """正则表达式替换里面的true和false"""
        string_after = re.sub("false", "False", string_before[0])
        string_after = re.sub("true", "True", string_after)
        item_list = eval(string_after)
        """并把结果返回到管道里"""
        self.crawl_num += 1
        for unit in item_list:
            item['tmall_list'] = unit
            self.goods_num += 1
            yield item
        print "当前爬取了", self.crawl_num, "个页面\t",\
            "当前爬取了", self.goods_num, "条商品信息"
        pass
