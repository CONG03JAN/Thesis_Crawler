# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import Crawler.items
import json
import codecs
import pymongo


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
    def __init__(self):
        client = pymongo.MongoClient("localhost", 27017)
        db = client.Thesis
        self.CateList = db.CateList

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理 """

        if isinstance(item, Crawler.items.CateList):
            try:
                self.CateList.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, Crawler.items.CateContent):
            try:
                pass
            except Exception:
                pass

        return item
