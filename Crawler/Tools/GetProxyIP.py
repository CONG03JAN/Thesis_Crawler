# -*- coding: utf-8 -*-

import json
import requests
import codecs
import re


def getProxyIP(num):
    """ 通过API获取代理IP地址"""

    print("\n")
    print("Update ProxyIP ......")
    print("\n")

    ProxyIP = []
    fp = codecs.open('./Tools/proxyip.json', 'w', encoding='utf-8')
    api = 'http://piping.mogumiao.com/proxy/api/get_ip_al?appKey=8242cd21d1274112b8dbd8793e6f4876&count=' + str(num) + '&expiryDate=5&format=1'
    response = requests.get(api)
    json_data = json.loads(response.text)
    results = json_data['msg']

    for result in results:
        ip = result['ip']
        port = result['port']
        proxyIP = str(ip) + ':' + str(port)
        if checkProxyIP(proxyIP):
            it = {'IP': ip, 'Port': port}
            ProxyIP.append(it)

    # 将有效的代理IP地址写入Json文件
    json.dump(ProxyIP, fp, ensure_ascii=False, indent=4)
    fp.close()


def checkProxyIP(proxyIP):
    """ 检测代理IP地址是否有效 """

    try:
        res = requests.get(
            'http://www.coffeexc.com/', proxies={"http": proxyIP}, timeout=2)
    except:
        print('Connect Failed http://' + proxyIP)
        return False
    else:
        print('Connect Success http://' + proxyIP)
        return True

if __name__ == "__main__":
    getProxyIP(3)
