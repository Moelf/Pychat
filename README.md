Pychat
======
An WeChat SDK for `Official Account` written in `Python` + `web.py` (run on SAE primely) 
Author: [Jerry Ling](https://github.com/jerryling315)
# Getting start
To use this SDK, you will need an **account** on WeChat's **Media-Platform**, you can register [here](http://mp.weixin.qq.com).
`For short, *MP* will be refers to **Media-Platform** from now on.
You should have basic knowledge on how WeChat's service works(such as how to auth the server), for more [information](http://mp.weixin.qq.com/wiki/index.php?title=%E6%8E%A5%E5%85%A5%E6%8C%87%E5%8D%97)
####\#Note:
There is certain code in the files  written only for [Sina SAE](http://sae.sina.com.cn/), I will point them out in the following explanation.
## 1. How *MP* works
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
## 2. How Pychat works
The response file in `Pychat` is:
>inter.py

located in the root dictionary.

###Using web.py indexing
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

###Using web.py and lxml to process POSTed data
```python
def __init__(self):  
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates') 
        self.render = web.template.render(self.templates_root)
        post_get = web.data()  # get POST data from WeChat
        post_xml = etree.fromstring(post_get)  # process the POST data with lxml
        self.xml_ins = XmlMsg(post_xml.find("ToUserName").text, #creating instance
                              post_xml.find("FromUserName").text,
                              post_xml.find("MsgType").text,
                              post_xml.find("CreateTime").text
```
You can easily get everything you need in the XML through `.find(STRING)` method in the `post_xml` now.
###Send the response 
Use the XML format mentioned in the I Chapter to response.

##3.(Truly) Tricky Template rendering
P.s The thing f\*\*\*ed me most at first is the template rendering, so don't be upset if it confused you too before reading the doc.
For sure there is web.py [explanation](http://webpy.org/docs/0.3/templetor) on template; feel free to check it since I won't go too detailed here.

*Check how to load `templates` dictionary and render in the previous section if you forget how to do so.*


Let's see on example of the template `.xml` file:
```xml
$def with (toUser,fromUser,createTime,content) #the args here will be used to take over the variables following 
<xml>
    <ToUserName>
        <![CDATA[$toUser]]> # the $toUser here will be replaced by the toUser above
    </ToUserName>
    <FromUserName>
        <![CDATA[$fromUser]]>
    </FromUserName>
    <CreateTime>
        $createTime
    </CreateTime>
    <MsgType>
        <![CDATA[text]]>
    </MsgType>
    <Content>
        <![CDATA[$:content]]>
    </Content>
</xml>
```
since we have defined:
>self.render = web.template.render(self.templates_root) 

When we want to `return`(reply) in the format, the only thing we need to do is:
```python
return self.render.reply_text("FRomuser",
                              "TOuser",
                              int(time.time()),
                              "CONTENT AS STRING"
        )
```
and the resultant XML would be:
```xml
$def with (toUser,fromUser,createTime,content)
<xml>
    <ToUserName>
        <![CDATA[TOuser]]>
    </ToUserName>
    <FromUserName>
        <![CDATA[FRomuser]]>
    </FromUserName>
    <CreateTime>
        123123 # the time would be int
    </CreateTime>
    <MsgType>
        <![CDATA[text]]>
    </MsgType>
    <Content>
        <![CDATA[CONTENT AS STRING]]>
    </Content>
</xml>
```
***One more thing***
see how I used:

> <\![CDATA\[$:content]]>

the very **":"** is crucial. It means `not using HTML escaping`. Thus "<" will not be turned into "%3C" in the result. For more on [escaping](http://webpy.org/docs/0.3/templetor#escaping).

##4.Tips
1. The `str` will just works fine for the result returned to WeChat server, thus if you want to have multiple(and not constant) content, say, `items` in the `news` MsgType, you will want to convert the `XML` into `str` and then perform the regular manipulation for string.
