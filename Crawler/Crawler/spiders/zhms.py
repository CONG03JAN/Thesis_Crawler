# -*- coding: utf-8 -*-
import scrapy
import Crawler.items


class ZhmsSpider(scrapy.Spider):
    name = 'zhms'
    allowed_domains = ['zhms.cn']
    start_page_num = '1'
    start_url = 'http://www.zhms.cn/cp/_1_' + start_page_num
    home_url = 'http://www.zhms.cn'
    pageLimit = 6690   # 定义爬取页面数
    pageCnt = 1
    itemCnt = 1
    print("\033[0;32m\t [ ------------ 爬虫程序启动成功 ------------ ] \033[0m")
    print("\n 爬取页面目标: " + str(pageLimit) + "\n\n")

    def start_requests(self):
        """ 构造爬虫初始请求 """
        return [
            scrapy.FormRequest(self.start_url, callback=self.cateList_parse)
        ]

    def cateList_parse(self, response):
        """ 爬取每个页面的美食项目 """

        # 构造需要数据的 XPath 表达式
        nextUrlRegx = '//a[@class="m-page-next"]/@href'
        cateNameRegx = '/html/body/div[3]/div[3]/div[1]/ul/li/div[1]/a/text()'
        cateUrlRegx = '/html/body/div[3]/div[3]/div[1]/ul/li/a/@href'

        # 获取该页面所有的项目名字以及链接
        cateNames = response.xpath(cateNameRegx).extract()
        cateUrls = response.xpath(cateUrlRegx).extract()

        for (cateName, cateUrl) in zip(cateNames, cateUrls):
            if cateName and cateUrl:
                # 构造存储数据的 CateList Item
                CateList = Crawler.items.CateList()
                CateList['cateID'] = self.itemCnt
                self.itemCnt += 1
                CateList['cateName'] = cateName
                CateList['cateUrl'] = self.home_url + cateUrl
                yield CateList

        print("\n\033[0;32m\t [ ------------ 已爬取项目数：" + str(self.itemCnt) + " ------------ ] \033[0m\n")

        # 获取下一页的链接并加入待爬取列表
        nextUrls = response.xpath(nextUrlRegx).extract()
        if nextUrls and self.pageCnt < self.pageLimit:
            # 只爬取指定数目的页面
            self.pageCnt += 1
            nextUrl = self.home_url + nextUrls[0]
            yield scrapy.Request(nextUrl, callback=self.cateList_parse)

    def parse(self, response):
        pass
