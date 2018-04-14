# -*- coding: utf-8 -*-

import json
import codecs
from fake_useragent import UserAgent


def getUserAgent(num):
    """ 获取num个UserAgent防反爬虫 """

    fp = codecs.open('user_agents.json', 'w', encoding='utf-8')

    agents = []

    ua = UserAgent()

    for i in range(num):
        it = ua.random
        print(it)
        agent = {
            'ua': it
        }
        agents.append(agent)

    json.dump(agents, fp, ensure_ascii=False, indent=4)

    fp.close()

getUserAgent(100)
