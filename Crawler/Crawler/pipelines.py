# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import Crawler.items
import json
import codecs
import pymongo
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import scrapy
from scrapy import log


class CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonPipleline(object):
    def __init__(self):
        self.fp = codecs.open('CateList.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理 """

        if isinstance(item, Crawler.items.CateList):
            try:
                pass
            except Exception:
                pass
        elif isinstance(item, Crawler.items.CateContent):
            try:
                pass
            except Exception:
                pass

        self.fp.close()
        return item


class MongoDBPipleline(object):
    """ MongoDB 数据库存储管道 """

    def __init__(self):
        """ 数据库初始化 """

        # 链接数据库
        client = pymongo.MongoClient("localhost", 27017)
        db = client.Thesis

        # 定义 CateList 集合
        self.CateList = db.CateList
        self.CateContent = db.CateContent

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理 """

        if isinstance(item, Crawler.items.CateList):
            # 美食列表数据存储
            try:
                self.CateList.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, Crawler.items.CateContent):
            # 美食详情数据存储
            try:
                self.CateContent.insert(dict(item))
            except Exception:
                pass

        return item


class ImgPipeline(ImagesPipeline):
    """ 图片存储管道定义 """

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]  # ok判断是否下载成功
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item
