# coding: UTF-8
# execfile('all_req.py')

import web  # 导入依赖的web.py hash time os lxml
import hashlib
import time
import os
from lxml import etree


class XmlMsg():  # 创建对象XmlMsg用于管理Decode后的XML
    def __init__(self, Tousername, Fromusername, Msgtype, Msgid, Createtime):  # 使用不定参数
        self.tousername = Tousername
        self.fromusername = Fromusername
        self.msgtype = Msgtype
        self.msgid = Msgid
        self.createtime = Createtime


class MpRobot():
    def __init__(self):  # 初始化MpRobot对象的变量
        self.app_root = os.path.dirname(__file__)  # 根据Sina设置app的根目录
        self.templates_root = os.path.join(self.app_root, 'templates')  # 根据web.py设置templates根目录
        self.render = web.template.render(self.templates_root)  # 设置加载的render变量
        post_get = web.data()  # 获取POST来的原始数据
        post_xml = etree.fromstring(post_get)  # 用lxml解析原始数据
        self.xml_ins = XmlMsg(post_xml.find("ToUserName").text,  # 生产XmlMsg的实例xml_ins
                              post_xml.find("FromUserName").text,
                              post_xml.find("MsgType").text,
                              post_xml.find("CreateTime").text,
                              post_xml.find("MsgId").text
        )
        if self.xml_ins.msgtype == "text":  # 根据需求自行添加内容, 参考微信封装
            self.xml_ins.content = post_xml.find("Content").text

    def POST(self):
        if self.xml_ins.msgtype == "text":
            return self.send_text(u"程序猿君正在尝试将公众平台从PHP的plate-form转移至Python, 我猜你刚刚大概说了：" + self.xml_ins.content)

        else:
            return self.send_text("人家暂时还不支持回复此种消息类型啦＞_＜~")  # 注意标点, UTF-8

    def send_text(self, content):  # 发送text, 用render.reply_text 封装
        return self.render.reply_text(self.xml_ins.fromusername,
                                      self.xml_ins.tousername,
                                      int(time.time()),
                                      content
        )

    def send_textimg(self, *args):
        articlenum = len(args) / 4  # 通过不定参数*args的长度处理得出article数量
        content = ""  # 初始化最终结果为空的string
        for items in range(0, articlenum):  # 循环过items长度
            content += str(self.render.article(*args[items * 4:items * 4 + 4]))  #取*args中对应的内容丢入article模板
        return self.render.reply_imgtext(self.xml_ins.fromusername,  #依次丢入图文模板
                                         self.xml_ins.tousername,
                                         int(time.time()),
                                         articlenum,
                                         content)