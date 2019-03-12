# -*- coding: utf-8 -*-
from pymongo import MongoClient
import re
import redis


class JdspiderPipeline(object):

    def __init__(self):
        super(JdspiderPipeline, self).__init__()
        self.mongo = MongoClient('localhost', 27017)
        self.jd_db = self.mongo['jdspider']
        pass

    def process_item(self, item, spider):
        if re.match('jd_', spider.name):
            json_data = dict(item)
            jd_col = self.jd_db['jingdong_data']
            jd_col.insert(json_data['jd_data'])
            return item
        else:
            return item


"""职责是将item中商品详情的URL存放到Redis中"""
class TmalllistspiderPipeline(object):

    def __init__(self):
        self.num = 0
        self.db_index = {
            'tmall_detail': 15,  # 商品详情地址数据库
            'tmall_rate': 14,  # 商品评论地址数据库
        }
        self.redis__detail_db = redis.Redis(host="localhost", port=6379, db=self.db_index['tmall_detail'])
        self.redis_rate_db = redis.Redis(host="localhost", port=6379, db=self.db_index['tmall_rate'])

    """商品的详细地址要在这里处理,将它放在Redis中"""
    def process_item(self, item, spider):
        if spider.name == 'tmall_list_spider':
            dict_data = dict(item)  # 转换成字典数据类型
            # tmall_detail_url = dict_data['tmall_list']['url']
            tmall_detail_item_id = dict_data['tmall_list']['item_id']
            tmall_detail_seller_id = dict_data['tmall_list']['seller_id']
            tmall_rate_id = {
                'item_id': tmall_detail_item_id,
                'seller_id': tmall_detail_seller_id
            }
            tmall_detail_id = {
                'item_id': tmall_detail_item_id
            }
            self.redis__detail_db.lpush('tmall_detail_id', tmall_detail_id)
            self.redis_rate_db.lpush('tmall_rate_id', tmall_rate_id)
            self.num += 1
            # print "处理了", self.num, "条item的URL"
            return item
        else:
            return item


"""职责是将管道中的item存放到MongoDB数据库中"""
class TmalllistMongoPipeline(object):

    def __init__(self):
        """建立一个数据库链接"""
        self.client = MongoClient(host='localhost', port=27017)

        """选择连接哪个数据库,如果没有则会自动创建"""
        self.tmalldb = self.client['tmallspider']

        """选择打开哪一个collection,如果没有则会创建collection"""
        self.tmall_list = self.tmalldb['tmall_data']

    def process_item(self, item, spider):
        if spider.name == 'tmall_list_spider':
            json_data = dict(item)  # 转换成字典数据类型
            """往collection中插入数据,插入的数据是字典类型"""
            self.tmall_list.insert(json_data['tmall_list'])
            return item
        else:
            return item


class TmallDetailPipeline(object):
    def __init__(self):
        """建立一个数据库链接"""
        self.client = MongoClient(host='localhost', port=27017)

        """选择连接哪个数据库,如果没有则会自动创建"""
        self.detaildb = self.client['tmallspider']

        """选择打开哪一个collection,如果没有则会创建collection"""
        self.tmall_detail = self.detaildb['tmall_detail_comp']

    def process_item(self, item, spider):
        if spider.name == 'tmall_detail_spider':
            # json_data = dict(item)  # 转换成字典数据类型
            """往collection中插入数据,插入的数据是字典类型"""
            self.tmall_detail.insert(item)
            return item
        else:
            return item


class TmallRateSpiderPipeline(object):
    def __init__(self):
        """建立一个数据库链接"""
        # self.client = MongoClient(host='119.29.201.76', port=27017)
        self.client = MongoClient(host='localhost', port=27017)

        """选择连接哪个数据库,如果没有则会自动创建"""
        self.tmalldb = self.client['tmallspider']

        """选择打开哪一个collection,如果没有则会创建collection"""
        self.tmall_rate = self.tmalldb['tmall_rate_compu']
        pass

    def process_item(self, item, spider):
        if spider.name == 'tmall_rate_spider':
            # json_data = dict(item)  # 转换成字典数据类型
            """往collection中插入数据,插入的数据是字典类型"""
            self.tmall_rate.insert(item)
            return item
        else:
            return item


class TaobaoPipeline(object):

    def __init__(self):
        client = MongoClient('localhost', 27017)
        mongodb = client['taobaospider']
        self.redisdb = redis.Redis('localhost', 6379, 0)
        self.Item = mongodb['taobao_data']
        self.goods_num = 0
        pass

    def process_item(self, item, spider):
        if(spider.name=='taobao_list_spider'):
            self.Item.insert(item)
            self.redisdb.rpush("Item_id",item["item_id"])
            self.goods_num += 1
            print '当前爬取的商品ID为:', item["item_id"], \
                '\t当前爬取了', self.goods_num, '条商品信息'
            return item
        else:
            return item


class TaobaoPipelineDetail(object):

    def __init__(self):
        client = MongoClient('localhost', 27017)
        mongodb = client['taobaospider']
        self.Item = mongodb['taobao_data']
        pass

    def process_item(self, item, spider):
        if(spider.name == 'taobao_detail_spider'):
            def item_dice(item):
                item_dict = {}
                Item = item['list'][0]['v']
                for i in range(0, len(Item)):
                    item_dict[Item[i]['k']] = Item[i]['v']
                return item_dict
            Item = item_dice(item)
            self.Item.update({'item_id':item['item_id']}, {"$set":{'detail':Item}}, multi=True)
            return Item
        else:
            return item
