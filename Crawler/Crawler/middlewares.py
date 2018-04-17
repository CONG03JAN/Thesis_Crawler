# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import json
import codecs
import requests
import Tools.ProxyIP
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class ProxyMiddleware(object):
    """ 随机更换 IP 代理 """

    proxy_list = []  # 代理池
    ProxyIPNum = 10  # 每次跟新的代理数

    def load_proxy_list(self):
        """ 从 proxyip.json 文件中载入代理地址 """

        with codecs.open('./Tools/proxyip.json', 'r', encoding='utf-8') as fp:
            json_data = json.loads(fp.read())
            for it in json_data:
                self.proxy_list.append(it)
        fp.close()

    def process_request(self, request, spider):
        """ 为每一次 Request 载入一个代理IP """

        self.load_proxy_list()  # 载入代理地址

        # 随机选择代理IP并格式化代理地址
        ip = random.choice(self.proxy_list)
        proxy = "HTTP://" + ip['IP'] + ":" + ip['Port']

        ipIsOk = True  # 标记是否超过尝试次数

        cnt = 1
        while Tools.ProxyIP.checkProxyIP(proxy) is False:
            if cnt > self.ProxyIPNum:
                ipIsOk = False
                break
            else:
                cnt += 1

            print("\n\033[0;31m\t [ ------------ 代理IP " + str(ip) +
                  " 连接超时 ------------ ] \033[0m\n")
            ip = random.choice(self.proxy_list)
            proxy = "HTTP://" + ip['IP'] + ":" + ip['Port']

        print("\n\033[0;34m\t [ ------------ 代理IP选择尝试次数: " + str(cnt) +
              " ------------ ] \033[0m\n")

        # 超过尝试次数，更新代理池，并选择一个可用代理
        if ipIsOk is False:
            Tools.ProxyIP.getProxyIP(self.ProxyIPNum)
            self.proxy_list = []
            self.load_proxy_list()
            ip = random.choice(self.proxy_list)
            proxy = "HTTP://" + ip['IP'] + ":" + ip['Port']
        else:
            print("\n\033[0;32m\t [ ------------ 代理IP " + str(ip) +
                  " 连接成功 ------------ ] \033[0m\n")

        request.meta['proxy'] = proxy


class RotateUserAgentMiddleware(UserAgentMiddleware):
    """ 随机更换 User-Agent """

    def __init__(self, user_agent=''):
        self.fp = codecs.open(
            './Tools/user_agents.json', 'r', encoding='utf-8')
        self.user_agent = user_agent
        json_data = json.loads(self.fp.read())
        self.fp.close()
        user_agent_list = []
        for it in json_data:
            user_agent_list.append(it['ua'])
        self.user_agent_list = user_agent_list

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        if ua:
            request.headers.setdefault('User-Agent', ua)


class CrawlerSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CrawlerDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
