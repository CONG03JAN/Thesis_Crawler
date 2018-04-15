# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CateList(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    cateName = scrapy.Field()  # 存储美食名字
    cateUrl = scrapy.Field()  # 存储美食详情链接


class CateContent(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 美食详情页爬取项目
    cateName = scrapy.Field()
    cateStar = scrapy.Field()
    cateInfo = scrapy.Field()

    # 美食图片爬取项目
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()

    # 美食制作教程页爬取项目
    prepareTime = scrapy.Field()
    accomplishTime = scrapy.Field()
    mainMaterial = scrapy.Field()
    othersMaterial = scrapy.Field()
    makeStep = scrapy.Field()
