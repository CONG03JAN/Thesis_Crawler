# -*- coding: utf-8 -*-

import json
import codecs
from fake_useragent import UserAgent


def getUserAgent(num):
    """ 获取num个UserAgent防反爬虫 """

    fp = codecs.open('./Tools/user_agents.json', 'w', encoding='utf-8')

    agents = []
    ua = UserAgent()

    for i in range(num):
        it = ua.random
        print(it)
        agent = {'ua': it}
        agents.append(agent)

    json.dump(agents, fp, ensure_ascii=False, indent=4)
    fp.close()


if __name__ == "__main__":
    getUserAgent(100)
    print(
        "\033[0;32m\t [ ------------ User-Agent 列表生成成功 ------------ ] \033[0m")
