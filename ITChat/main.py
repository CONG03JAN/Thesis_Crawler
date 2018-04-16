import pymongo
import re
import itchat
import Search


client = pymongo.MongoClient("localhost", 27017)
db = client.Thesis
dbCateList = db.CateList
dbCateContent = db.CateContent

startString = "输入：菜谱推荐 + 关键词（空格分割）给您推荐菜谱\n（例如：菜谱推荐 鸡蛋）\n输入：做法 + 菜谱名 给你介绍美食的详细做法\n（例如：做法 西红柿炒鸡蛋）\n"


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    user = msg.fromUserName
    try:
        msgContent = msg['Text']
        print(msgContent)
        msgLen = len(msgContent)
        # 长度不够，非法输入
        if msgLen <= 2:
            sendMsg("您好，亲爱的:\n" + startString, user, 1)
        # 菜谱推荐
        elif msgContent[0:4] == "菜谱推荐" or msgContent[0:4] == "推荐菜谱":
            msgKey = msgContent[5:]
            print(msgKey)
            results = Search.getSuggestionsByName(msgKey)

            if results:
                for result in results:
                    sendString = ""
                    # print(result)
                    cateID = result[0]
                    cateName = result[1]
                    sendString += "美食名: " + cateName
                    sendString += '\n'
                    cateInfo = ""
                    cateStar = "★ "
                    cateContent = Search.getInfoById(cateID)
                    if cateContent:
                        cateInfo = "美食介绍: " + cateContent['cateInfo']
                        cateStar = "美食评星: "
                        for i in range(cateContent['cateStar']):
                            cateStar += "★ "
                    sendString += cateStar
                    sendString += '\n'
                    sendString += cateInfo
                    sendString += '\n'
                    sendMsg(sendString, user, 1)
                    if cateContent:
                        sendString = "./" + cateContent['image_paths']
                        print(sendString)
                        sendMsg(sendString, user, 0)

                print(sendString)

            else:
                sendMsg("很抱歉我们的菜谱里没有这道菜 ^_^ \n", user, 1)
            pass
        # 美食做法信息
        elif msgContent[0:2] == "做法":
            pass
        # 非法信息
        else:
            sendMsg("您好，亲爱的:\n" + startString, user, 1)
        print("消息发送成功 ！！！")
    except:
        print("消息发送失败 ！！！")
    #return msg.text


def sendMsg(sendString, sendUser, msgType):
    """ 发送指定信息给用户 """

    if msgType == 1:  # msgType 为 1 时为文本信息
        itchat.send(sendString, toUserName=sendUser)
    else:  # msgType 为 2 时为图片信息
        itchat.send('@img@%s' % sendString, toUserName=sendUser)


itchat.auto_login()
# itchat.auto_login(hotReload=True)
itchat.run()
