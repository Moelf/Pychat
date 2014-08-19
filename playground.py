# coding: UTF-8
# execfile('all_req.py')

import web  # 导入依赖的web.py hash time os lxml
import hashlib
import time
import os
from lxml import etree
from xml.sax.saxutils import unescape


app_root = os.path.dirname(__file__)  # 根据Sina设置app的根目录
templates_root = os.path.join(app_root, 'templates')  # 根据web.py设置templates根目录
render = web.template.render(templates_root)  # 设置加载的render变量


def send_text(content):
    return render.test("fromuser",
                       "touser",
                       int(time.time()),
                       content
    )

a = render.hh()

print send_text(a)