Pychat
======
A WeChat SDK for `Official Account` written in `Python` + `web.py` (run on SAE primely) 
Author: [Jerry Ling](https://github.com/jerryling315)
# Getting start
To use this SDK, you will need an **account** on WeChat's **Media-Platform**, you can register at [here](http://mp.weixin.qq.com).
`For short, **Media-Platform** will be *MP* from now on.
You should have basic knowledge on how does WeChat's service work(such as how to auth the server), for more [information](http://mp.weixin.qq.com/wiki/index.php?title=%E6%8E%A5%E5%85%A5%E6%8C%87%E5%8D%97)
####\#Note:
There is certain code in the files  written only for [Sina SAE](http://sae.sina.com.cn/), I will point them out in the following explanation.
## 1. How does *MP* work?
After your server is verified for *MP*, the *MP* server will send every message(include `Event` such as subscription ) to your server through `POST` method. And the message will be parsed in the `XML` format.
Here's a `XML` example for a **Text Message**:
```xml
<xml>
 <ToUserName><![CDATA[toUser]]></ToUserName>
 <FromUserName><![CDATA[fromUser]]></FromUserName> 
 <CreateTime>1348831860</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[a test from user]]></Content>
 <MsgId>1234567890123456</MsgId>
</xml>
```
And if your server reply the message to the same person(verified using `ToUserName` and `FromUserName`) within 5 seconds, and in appropriate format.

Such as a **Text** reply:
```xml
<xml>
    <ToUserName><![CDATA[toUser]]></ToUserName>
    <FromUserName><![CDATA[fromUser]]></FromUserName>
    <CreateTime>12345678</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[hello world]]></Content>
</xml>
```
Again you can find all these on [*MP*'s wiki](http://mp.weixin.qq.com/wiki/index.php)
## 2. How does Pychat work?
The response file in `Pychat` is:
>inter.py

located in the root dictionary.

###The web.py
I used `web.py` in the SDK to handle the request, and `web.py` also provides a way to **mapping** the **urls** on the server.The file is:
>index.wsgi

in the file:
```python
# coding: UTF-8
import os  #nessary for every one
import sae  #is only needed for Sina SAE
import web  #this is web.py
from inter import MpRobot  #from the inter.py import MpRobot class

urls = (            #map the url:/ with the MpRobot class
    '/', 'MpRobot'
)

app_root = os.path.dirname(__file__)  #asign the path for files
templates_root = os.path.join(app_root, 'templates')  #asign the path to templates folder
render = web.template.render(templates_root)  #load web.py render

app = web.application(urls, globals()).wsgifunc()  #These two lines are only needed for Sina SAE to create app on its engine
application = sae.create_wsgi_app(app)             #
```


If you server located at `crap.sae.com.cn`, so its url would be `http://crap.sae.com.cn/`, now it's linked the class `MpRobot` .

For more information related to `web.py`, [click](http://webpy.org/cookbook/).

##Not finished yet : {
