# coding: UTF-8
# execfile('all_req.py')

import web  # 导入依赖的web.py hash time os lxml
import hashlib
import time
import os
from lxml import etree
import re  # 正则表达式


class XmlMsg():  # The object class for manage the "Msg"
    def __init__(self, Tousername, Fromusername, Msgtype, Createtime):
        self.tousername = Tousername
        self.fromusername = Fromusername
        self.msgtype = Msgtype
        self.createtime = Createtime


class MpRobot():
    def __init__(self):  # init the Response class
        self.app_root = os.path.dirname(__file__)  # Set the app root path
        self.templates_root = os.path.join(self.app_root, 'templates')  # Set Templates path for web.py
        self.render = web.template.render(self.templates_root)  # load render
        post_get = web.data()  # Get Msg from POST
        post_xml = etree.fromstring(post_get)  # use lxml to process POST data
        self.xml_ins = XmlMsg(post_xml.find("ToUserName").text,  # Create instance for Msg
                              post_xml.find("FromUserName").text,
                              post_xml.find("MsgType").text,
                              post_xml.find("CreateTime").text
        )
        if self.xml_ins.msgtype == "text":  # add Type as you need
            self.xml_ins.content = post_xml.find("Content").text
            self.xml_ins.msgid = post_xml.find("MsgId").text
        elif self.xml_ins.msgtype == "event":
            self.xml_ins.event = post_xml.find("Event").text
        else:
            pass


    def POST(self):
        if self.xml_ins.msgtype == "text":
            if self.xml_ins.content in u"?？？" or "help" in self.xml_ins.content:  # use Unicode for Chinese
                return self.asking()
            elif re.compile(r"recent", re.I).search(self.xml_ins.content):  # Regular Expression
                return self.recent()
            else:
                return self.send_text("收到您的消息啦")
        elif self.xml_ins.event == "subscribe":
            return self.greeting()
        else:
            return self.send_text("人家暂时还不支持回复此种消息类型啦＞_＜~")  # UTF-8

    def send_text(self, content):  # send text, use render to load
        return self.render.reply_text(self.xml_ins.fromusername,
                                      self.xml_ins.tousername,
                                      int(time.time()),
                                      content
        )

    def send_textimg(self, *args):
        articlenum = len(args) / 4  # calculate the number of items through *args
        content = ""  # init the result
        for items in range(0, articlenum):  # loop through number of items
            content += str(self.render.article(*args[items * 4:items * 4 + 4]))  # use the 4 args one time
        return self.render.reply_imgtext(self.xml_ins.fromusername,  # add into result
                                         self.xml_ins.tousername,
                                         int(time.time()),
                                         articlenum,
                                         content)

    def greeting(self):
        return self.send_textimg("欢迎关注!",
                                 "欢迎关注!",
                                 "http://mmbiz.qpic.cn/mmbiz/YiagimTcpcPRkj8QSQ/0",
                                 "http://mp.weixin.qq.com/s?__biz=25926fd1856c06305640c790f929c5b#rd",
                                 "工作平台指",
                                 "欢迎关注! 这里有些有用的Tips和有助于提高平台工作效率的规范希望大家注意",
                                 "https://mmbiz.qlogo9uoSxniaP3ibRFD2TwdvCdBUCSOutiak8kQ/0",
                                 "http://mp.weixin.qq.com/s?__biz=MzA83753033fba91eb5dea2d385065df31#rd"
        )

    def asking(self):
        return self.send_textimg("Welcome to  !",
                                 "Welcome to  !",
                                 "https://mmbiz.qlogo.cn/mmbiz/YiagibTTfjHgxibAPsZDd2dwVHTUEvWQ5LSKklcYH0ibxd39IVphDgBMaib4xSvibhXH3nk4lRfFeOH9Q0T1Mue9AXbQ/0",
                                 "http://mp.weixin.qq.com/s?__biz=MzA4MDcxMDYzOQ==&mid=202620990&idx=1&sn=b0b3b2dc709fca7eeb1afb460384e944#rd",
                                 "工作平台指南以及规范",
                                 "欢迎关注! 这里有些有用的Tips和有助于提高平台工作效率的规范希望大家注意",
                                 "https://mmbiz.qlogo.cn/mmbiz/YiagibTTfjHgy9uoSxnUbyy6uQTjue8eOPLb15AAeoLialYENv8VyG9R6ibxfs4diaP3ibRFD2TwdvCdBUCSOutiak8kQ/0",
                                 "http://mp.weixin.qq.com/s?__biz=MzA4MDcxMDYzOQ==&mid=203540783&idx=1&sn=183753033fba91eb5dea2d385065df31#rd",
                                 "项目信息介绍",
                                 "项目信息介绍",
                                 "https://mmbiz.qlogo.cn/mmbiz/YiagibHPMRKDeKeul4diaa0CrR2xwVkyhbFuMGnXfNtM4WLKYfwzJS5J8jKpiabWCgA/0",
                                 "http://mp.weixin.qq.com/s?__biz=MzA4Mn=d4fc06fe40f096b2705482c4f512e49d#rd",
                                 "如何报名活动？",
                                 "如何报名活动？",
                                 "https://mmbiz.qlogo.cn/mmbiz/YiagibTTfjHgnYO9HPMRK0cceqrkvSMCteWOCRMomLjZhGDeYpaGDDd9eJOiaAfHl9IXGoHAIib2A/0",
                                 "http://mp.weixin.qq.com/s?__biz=MzA4MDcxMe67d66e6129a6e5cdb1c4d5bcb#rd"
        )

    def recent(self):
        return self.send_text(u"近期没有活动哒>_<")