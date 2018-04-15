# -*- coding: utf-8 -*-
import scrapy
import Crawler.items
import pymongo


class ZhmsContentSpider(scrapy.Spider):
    name = 'zhms_content'
    allowed_domains = ['zhms.cn']
    start_item_id = 1

    home_url = 'http://www.zhms.cn'
    itemLimit = 6  # 定义爬取项目数
    itemCnt = 1

    client = pymongo.MongoClient("localhost", 27017)
    db = client.Thesis
    dbCateList = db.CateList
    nowItem = dbCateList.find_one({"cateID": itemCnt})

    if nowItem:
        start_url = nowItem['cateUrl']
    else:
        start_url = "http://www.zhms.cn/cp/28/"

    print("\033[0;32m\t [ ------------ 爬虫程序启动成功 ------------ ] \033[0m")
    print("\n 爬取项目目标: " + str(itemLimit) + "\n\n")

    def start_requests(self):
        """ 构造爬虫初始请求 """
        return [
            scrapy.FormRequest(self.start_url, callback=self.cateInfo_parse)
        ]

    def cateInfo_parse(self, response):
        """ 爬取每个美食项目的介绍 """

        # 构造需要数据的 XPath 表达式
        cateNameRegx = '/html/body/div[3]/div[2]/div/h1/text()'
        cateStarRegx = '//i[@class="ico-star ico-star-ct"]'
        cateInfoRegx = '/html/body/div[3]/div[2]/h2//text()'
        image_urlsRegx = '/html/body/div[3]/div[2]/img/@src'
        cateMakeUrlsRegx = '/html/body/div[3]/div[3]/div[1]/div[2]/ul/li/a/@href'

        # 获取该页面所有的项目名字以及链接
        cateName = response.xpath(cateNameRegx).extract()
        cateStar = response.xpath(cateStarRegx).extract()
        cateInfo = response.xpath(cateInfoRegx).extract()
        image_urls = response.xpath(image_urlsRegx).extract()
        cateMakeUrls = response.xpath(cateMakeUrlsRegx).extract()

        CateContent = Crawler.items.CateContent()

        CateContent['cateID'] = self.itemCnt

        if cateName:
            CateContent['cateName'] = cateName[0]
        else:
            CateContent['cateName'] = "None"

        if cateStar:
            CateContent['cateStar'] = len(cateStar)
        else:
            CateContent['cateStar'] = -1

        if cateInfo:
            CateContent['cateInfo'] = "".join(cateInfo)
        else:
            CateContent['cateInfo'] = "None"

        if image_urls:
            CateContent['image_urls'] = image_urls[0].split('?', 1)[0]
        else:
            pass

        if cateMakeUrls:
            cateMakeUrl = self.home_url + cateMakeUrls[0]
            yield scrapy.Request(
                url=cateMakeUrl,
                meta={'item': CateContent},
                callback=self.cateMake_parse)
        else:
            yield CateContent
            self.itemCnt += 1
            if self.itemCnt < self.itemLimit:
                nowItem = self.dbCateList.find_one({"cateID": self.itemCnt})
                while True:
                    if nowItem:
                        break
                    else:
                        self.itemCnt += 1
                        nowItem = self.dbCateList.find_one({
                            "cateID":
                            self.itemCnt
                        })
                nextItemUrl = nowItem['cateUrl']
                print("---------------------")
                print(type(nextItemUrl))
                yield scrapy.Request(nextItemUrl, callback=self.cateInfo_parse)

        print("\n")

        # 获取下一个项目的链接并加入待爬取列表

    def cateMake_parse(self, response):
        """ 爬取每个美食项目的制作教程 """

        # 构造需要数据的 XPath 表达式
        prepareTimeRegx = '/html/body/div[3]/div[2]/div[1]/div[1]/div/dl/dd[1]/span/text()'
        accomplishTimeRegx = '/html/body/div[3]/div[2]/div[1]/div[1]/div/dl/dd[2]/span/text()'
        mainMaterialsRegx = '//*[@id="mainMaterial"]/ul/li'
        othersMaterialsRegx = '/html/body/div[3]/div[2]/div[1]/div[3]/ul/li'
        makeStepsRegx = '/html/body/div[3]/div[2]/div[1]/div[4]/ul/li'

        # 获取该页面所有的项目名字以及链接
        prepareTime = response.xpath(prepareTimeRegx).extract()
        accomplishTime = response.xpath(accomplishTimeRegx).extract()
        mainMaterials = response.xpath(mainMaterialsRegx)
        othersMaterials = response.xpath(othersMaterialsRegx)
        makeSteps = response.xpath(makeStepsRegx)

        CateContent = response.meta['item']

        if prepareTime:
            CateContent['prepareTime'] = prepareTime[0]
        else:
            CateContent['prepareTime'] = "None"

        if accomplishTime:
            CateContent['accomplishTime'] = accomplishTime[0]
        else:
            CateContent['accomplishTime'] = "None"

        if mainMaterials:
            mainMaterial = ""
            for it in mainMaterials:
                s = it.xpath(".//text()").extract()
                if s:
                    mainMaterial += " ".join(s)
                else:
                    if mainMaterial:
                        pass
                    else:
                        mainMaterial = "None"
                    break
            CateContent['mainMaterial'] = mainMaterial
        else:
            CateContent['mainMaterial'] = "None"

        if othersMaterials:
            othersMaterial = ""
            for it in othersMaterials:
                s = it.xpath(".//text()").extract()
                if s:
                    othersMaterial += " ".join(s)
                else:
                    if othersMaterial:
                        pass
                    else:
                        othersMaterial = "None"
                    break
            CateContent['othersMaterial'] = othersMaterial
        else:
            CateContent['othersMaterial'] = "None"

        if makeSteps:
            makeStep = ""
            for it in makeSteps:
                s = it.xpath("./h2/text()").extract()
                if s:
                    makeStep += "\n".join(s)
                else:
                    if makeStep:
                        pass
                    else:
                        makeStep = "None"
                    break
                s = it.xpath("./h3/text()").extract()
                if s:
                    makeStep += "\n".join(s)
                else:
                    if makeStep:
                        pass
                    else:
                        makeStep = "None"
                    break
            CateContent['makeStep'] = makeStep
        else:
            CateContent['makeStep'] = "None"

        print("\n")

        yield CateContent
        self.itemCnt += 1
        if self.itemCnt < self.itemLimit:
            nowItem = self.dbCateList.find_one({"cateID": self.itemCnt})
            while True:
                if nowItem:
                    break
                else:
                    self.itemCnt += 1
                    nowItem = self.dbCateList.find_one({
                        "cateID": self.itemCnt
                    })
            nextItemUrl = nowItem['cateUrl']
            yield scrapy.Request(nextItemUrl, callback=self.cateInfo_parse)

    def parse(self, response):
        pass
