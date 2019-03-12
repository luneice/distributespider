# -*- coding: utf-8 -*-
import redis
import custom_settings as settings


"""
此处是避免反爬虫的，例如更换COOKIES和头部信息以及设置代理等
"""
# 爬虫代理处
class ProxyMiddleware(object):

    def __init__(self):
        # 如有必要则在此处初始化一些东西，例如建立数据库的连接
        self.redis_index = settings.redis_index
        # 连接到代理池数据库
        self.redis_db = redis.Redis('localhost', 6379, self.redis_index['proxy'])
        # 代理IP个数
        self.proxy_num = 0
        # 代理IP阀值
        self.proxy_minnum = 2
        # 代理池的IP准备
        self.init_proxy()
        pass

    # 代理池的准备
    def init_proxy(self):
        # 如果代理池IP数量少于规定数量，则更新代理池IP
        if self.proxy_num > self.proxy_minnum:
            return
        # 从文件中读取代理的IP并存入Redis代理数据库
        with open('./proxy.txt', 'r+') as proxy:
            proxy_list = proxy.readlines()
        for ip in proxy_list:
            proxy_item = 'https://' + ip.strip('\n')
            self.redis_db.lpush("https_proxy", proxy_item)
        # 再次获取代理的IP数量
        self.proxy_num = self.redis_db.llen('https_proxy')
        pass

    def get_proxy(self):
        # 如果代理IP少于阀值，则重新获取更多代理IP
        if self.proxy_num < self.proxy_minnum:
            self.init_proxy()
        proxy = self.redis_db.lpop('https_proxy')
        # 取一个代理IP则减一
        self.proxy_num -= 1
        print "成功取出了一个代理IP", proxy
        return proxy

    def add_proxy(self, proxy):
        # 归还一个代理IP则加一
        self.redis_db.lpush('https_proxy', proxy)
        self.proxy_num += 1
        pass

    """添加一些头部等信息并发起请求，响应结果会在process_response处理"""
    def process_request(self, request, spider):
        # 取出一个代理IP
        proxy = self.get_proxy()
        request.meta['proxy'] = proxy  # 设置代理
        return None

    # 如果代理服务器成功处理了请求，那么此代理IP有效，应该重新添加到代理池中
    def process_response(self, request, response, spider):
        # 将有效的代理IP归还
        proxy = request.meta['proxy']
        self.add_proxy(proxy)
        print proxy, "代理服务器成功请求了，因此此IP可用，将其归还到代理池中"
        return response
