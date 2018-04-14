# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CateList(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    cateName = scrapy.Field() # 存储美食名字
    cateUrl = scrapy.Field() # 存储美食详情链接

class CateContent(scrapy.Item):
    pass
