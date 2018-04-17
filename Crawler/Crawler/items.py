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
    cateID = scrapy.Field()  # 美食 ID


class CateContent(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    cateID = scrapy.Field()  # 美食 ID

    # 美食详情页爬取项目
    cateName = scrapy.Field()  # 美食名
    cateStar = scrapy.Field()  # 美食评星
    cateInfo = scrapy.Field()  # 美食介绍

    # 美食图片爬取项目
    image_urls = scrapy.Field()  # 美食图片 URL
    image_paths = scrapy.Field()  # 美食图片本地存储地址

    # 美食制作教程页爬取项目
    prepareTime = scrapy.Field()  # 准备时间
    accomplishTime = scrapy.Field()  # 完成时间
    mainMaterial = scrapy.Field()  # 主要食材
    othersMaterial = scrapy.Field()  # 辅料
    makeStep = scrapy.Field()  # 制作步骤
