# -*- coding: utf-8 -*-

import re
import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client.Thesis
dbCateList = db.CateList
dbCateContent = db.CateContent

def getInfoByName(inString):
    """ 通过关键字精确搜索数据库 """

    cateList = dbCateList.find()
    collection = cateList

    pattern = inString + '.*?'
    regex = re.compile(pattern)

    resultID = 0

    for item in collection:
        match = regex.search(item['cateName'])
        if match:
            resultID = item['cateID']
            break
        else:
            pass

    if resultID == 0:
        return None
    else:
        result = getInfoById(resultID)
        return result


def getSuggestionsByName(inString, itemLimit=5):
    """ 通过关键字模糊搜索数据库 """

    suggestions = []  # 搜索建议列表

    cateList = dbCateList.find()
    collection = cateList

    regxString = inString.split(" ")  # 空格分割关键字
    print(regxString)

    # pattern = '.*?'.join(regxString)  # 转换 'key word' to 'key.*?word'
    # regex = re.compile(pattern)  # 编译正则匹配表达式

    # 匹配
    itemCnt = 1

    for key in regxString:
        pattern = '.*?'.join(key)
        regex = re.compile(pattern)
        matchTmp = []
        for item in collection:
            match = regex.search(item['cateName'])
            if match:
                matchTmp.append(item)
        collection = matchTmp

    print("collection: \n")
    print(collection)

    if collection:
        for item in collection:
            cateName = clearData(item['cateName'])
            result = (item['cateID'], cateName)
            suggestions.append(result)
            if itemCnt > itemLimit:
                break
            else:
                itemCnt += 1

    return suggestions


def getInfoById(cateID):
    """ 通过给定 cateID 获取美食项目详细信息 """

    cateContent = dbCateContent.find({"cateID": cateID})
    if cateContent:
        return cateContent[0]
    else:
        return None

def clearData(inString):
    """ 清洗数据 """

    result = inString

    pattern = '.*?'.join("的做法")
    regxString = re.compile(pattern)
    match = regxString.search(inString)

    if match:
        result = inString.replace("的做法", "")

    pattern = '.*?'.join("的家常做法")
    regxString = re.compile(pattern)
    match = regxString.search(result)

    if match:
        result = result.replace("的家常做法", "")

    return result


if __name__ == "__main__":
    result = getSuggestionsByName("番茄 面")
    for it in result:
        print(it)
