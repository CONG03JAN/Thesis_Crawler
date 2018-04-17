# -*- coding: utf-8 -*-

import json
import requests
import codecs
import re


def getProxyIP(num):
    """ 通过API获取代理IP地址"""

    print("\n")
    print("\033[0;32m\t [ ------------ 正在更新代理池 ------------ ] \033[0m")
    print("\n")

    ProxyIP = []  # 存储可用代理 IP

    # 构造 API 地址
    appKey = '78e9d532e0cc43d182bb3bb278ed0486'
    api = 'http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=' + appKey + '&count=' + str(
        num) + '&expiryDate=0&format=1'

    # 获取代理 IP 地址
    response = requests.get(api)
    json_data = json.loads(response.text)
    results = json_data['msg']

    # 检测获取的代理 IP 有效性
    if results:
        for result in results:
            ip = result['ip']
            port = result['port']
            proxyIP = str(ip) + ':' + str(port)
            if checkProxyIP(proxyIP):
                print("\033[0;32m\t [ ------------ 有效IP代理: http://" + proxyIP +
                      " ------------ ] \033[0m")
                it = {'IP': ip, 'Port': port}
                ProxyIP.append(it)
            else:
                print("\033[0;31m\t [ ------------ 失效IP代理: http://" + proxyIP +
                      " ------------ ] \033[0m")

    # 将有效的代理 IP 地址写入 Json 文件, 若失败则不更改原 Json 文件
    if ProxyIP:
        print("\033[0;32m\t [ ------------ 代理池更新成功 ------------ ] \033[0m")
        fp = codecs.open('./Tools/proxyip.json', 'w', encoding='utf-8')
        json.dump(ProxyIP, fp, ensure_ascii=False, indent=4)
        fp.close()
    else:
        print("\033[0;31m\t [ ------------ 代理池更新失败 ------------ ] \033[0m")

    print("\n")
    print("\n")


def checkProxyIP(proxyIP):
    """ 检测代理IP地址是否有效 """

    testUrl = 'http://www.zhms.cn/'

    try:
        res = requests.get(testUrl, proxies={"http": proxyIP}, timeout=1.5)
    except:
        return False
    else:
        return True


if __name__ == "__main__":
    getProxyIP(3)
