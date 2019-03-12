# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    jd_data = scrapy.Field()
    pass


class TmallspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tmall_list = scrapy.Field()
    pass


class TmallRateItem(scrapy.Item):
    tmall_rate = scrapy.Field()
    pass


class TaobaoItem(scrapy.Item):
    Name = scrapy.Field()
    Location = scrapy.Field()
    Price = scrapy.Field()
    Sold = scrapy.Field()
    pass
