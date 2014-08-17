__author__ = 'ex'
# coding: UTF-8
#execfile('all_req.py')

import web  #导入依赖的web.py hash time os lxml
import hashlib
import time
import os
from lxml import etree


class XmlMsg():  #创建对象XmlMsg用于管理Decode后的XML
    def __init__(self, **kwargs):  #使用不定参数
        self.tousername = kwargs["tousername"]
        self.fromusername = kwargs["fromusername"]
        self.msgtype = kwargs["msgtype"]
        self.msgid = kwargs["msgid"]
        self.createtime = kwargs["createtime"]


class MpRobot():

    def __init__(self): #初始化MpRobot对象的变量
        self.app_root = os.path.dirname(__file__)  #根据Sina设置app的根目录
        self.templates_root = os.path.join(self.app_root, 'templates')  #根据web.py设置templates根目录
        self.render = web.template.render(self.templates_root)  #设置加载的render变量
        post_get = web.data() #获取POST来的原始数据
        post_xml = etree.fromstring(post_get) #用lxml解析原始数据
        self.xml_ins = XmlMsg(tousername = post_xml.find("ToUserName").text,  #生产XmlMsg的实例xml_ins
                              fromusername = post_xml.find("FromUserName").text,
                              msgtype = post_xml.find("MsgType").text,
                              createtime = post_xml.find("CreateTime").text,
                              msgid = post_xml.find("MsgId").text
                              )
        if self.xml_ins.msgtype == "text":  #根据需求自行添加内容, 参考微信信息封装
            self.xml_ins.content = post_xml.find("Content").text

    def POST(self):
        if self.xml_ins.msgtype == "text":
            return self.send_text(u"程序猿君正在尝试将公众平台从PHP的plateform转移至Python, 我猜你刚刚大概说了："+self.xml_ins.content)
        else:
            return self.send_text("人家暂时还不支持回复此种消息类型啦＞_＜~") #注意卖萌使用好标点, 不然unicode的UTF-8会解析错误



    def send_text(self, content):
        return self.render.reply_text(self.xml_ins.fromusername,
                                      self.xml_ins.tousername,
                                      int(time.time()),
                                      content
                                      )




