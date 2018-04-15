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

    ProxyIP = []
    fp = codecs.open('./Tools/proxyip.json', 'w', encoding='utf-8')
    appKey = '78e9d532e0cc43d182bb3bb278ed0486'
    api = 'http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=' + appKey + '&count=' + str(num) + '&expiryDate=0&format=1'
    response = requests.get(api)
    json_data = json.loads(response.text)
    results = json_data['msg']

    for result in results:
        ip = result['ip']
        port = result['port']
        proxyIP = str(ip) + ':' + str(port)
        if checkProxyIP(proxyIP):
            print("\033[0;32m\t [ ------------ 有效IP代理: http://" + proxyIP + " ------------ ] \033[0m")
            it = {'IP': ip, 'Port': port}
            ProxyIP.append(it)
        else:
            print("\033[0;31m\t [ ------------ 失效IP代理: http://" + proxyIP + " ------------ ] \033[0m")

    # 将有效的代理IP地址写入Json文件
    json.dump(ProxyIP, fp, ensure_ascii=False, indent=4)
    fp.close()
    print("\n")
    print("\033[0;32m\t [ ------------ 代理池更新成功 ------------ ] \033[0m")
    print("\n")


def checkProxyIP(proxyIP):
    """ 检测代理IP地址是否有效 """

    testUrl = 'http://ip.chinaz.com/getip.aspx'

    try:
        res = requests.get(testUrl, proxies={"http": proxyIP}, timeout=1.5)
    except:
        return False
    else:
        return True

if __name__ == "__main__":
    getProxyIP(3)
