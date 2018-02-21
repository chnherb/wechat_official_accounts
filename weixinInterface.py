#coding=utf8
'''
微信公众号入口
author:Huangbo
email:chnhuangbo@gmail.com
date:2017-09-23
'''

import hashlib
import web
import lxml
import time
import os
import sys
from lxml import etree
from facedetection import getImageInfo
from autoreply import getAnswer
from strutil import StrUtil
from mysqldbutil import MySQLDBUtil
import musicutil
import subscription

abspath = os.path.dirname(sys.argv[0])   
if not os.path.isdir(abspath):
    abspath = sys.path[0]
if not os.path.isdir(abspath):
    abspath = os.path.dirname(__file__)
os.chdir(abspath)
render = web.template.render(os.path.join(abspath, 'templates/'))

class WeixinInterface:
    def GET(self):
        # return render.reply_text('zhangsan','lisi',int(time.time()),u'哈哈哈哈哈哈')
        data = web.input()		# 获取输入参数
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        
        token="**********"				# 自己的token
        
        list=[token,timestamp,nonce]	# 字典序排序
        list.sort()
        
        sha1=hashlib.sha1()				# sha1加密算法
        map(sha1.update, list)
        hashcode=sha1.hexdigest()
        
        if hashcode == signature:		# 如果是来自微信的请求，则回复echostr
            return echostr				# print "true"
        
    def POST(self):
        str_xml=web.data()
        xml=etree.fromstring(str_xml)
        #提取信息
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        #模板渲染
        # return self.render.reply_text(fromUser,toUser,int(time.time()),u"大家好我现在还只会卖萌，你刚才说的是："+content)
        # test_data = '<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><MsgId>1234567890123456</MsgId></xml>'
        if msgType == 'text':
            content=xml.find("Content").text
            contentType,contentInfo = StrUtil.getcontenttype(content)
            if contentType == u'content':
                return render.reply_text(fromUser,toUser,int(time.time()),getAnswer(content))
            elif contentType == u'grade66':
                return render.reply_text(fromUser,toUser,int(time.time()),MySQLDBUtil.Select('grade',contentInfo))
            elif contentType == u'成绩':
                return render.reply_text(fromUser,toUser,int(time.time()),u'成绩查询功能已下架')
            elif contentType == u'音乐' or contentType == u'music':
                title_artist,album,url = musicutil.getmusic(contentInfo)
                if url != None and str(url).strip()!='':
                    return render.reply_music(fromUser,toUser,int(time.time()),title_artist,album,url)
                else:
                    return render.reply_text(fromUser,toUser,int(time.time()),u'检索失败，请重新输入关键字，如“音乐 千里之外周杰伦”')
            elif contentType == u'文章' or contentType == u'article':
                return subscription.getInfo(fromUser,toUser,contentInfo)
            else:
                return render.reply_text(fromUser,toUser,int(time.time()),getAnswer(content))
            # return (test_data)%(fromUser,toUser,int(time.time()),u"大家好我现在还只会卖萌，你刚才说的是："+content)
        elif msgType == 'event':
            if xml.find("Event").text == 'subscribe':#关注的时候的欢迎语
                return render.reply_text(fromUser, toUser, int(time.time()), u"谢谢你的关注，我现在除了能识别人的表情外还会卖萌，发送照片给我可以识别你的性别年龄心情，来试试~\n或者输入城市+天气如（南京天气）、笑话、音乐/music+空格+关键词可以获取音乐、文章/article+空格+关键词可以搜索公众号文章等等获取相关信息(+不用输入哦)，更多隐藏功能等你来发现~让我来陪你聊天吧")
        elif msgType == 'image':
            try:
                picurl = xml.find('PicUrl').text
                imageInfo = getImageInfo(picurl)
                # return (test_data)%(fromUser, toUser, int(time.time()), '图中人物性别为'+datas[0]+'\n'+'年龄为'+datas[1])
                return render.reply_text(fromUser, toUser, int(time.time()), imageInfo)
            except:
                return render.reply_text(fromUser, toUser, int(time.time()),  '识别失败，换张图片试试吧')   
        else:
            return render.reply_text(fromUser, toUser, int(time.time()), u"我现在还只会卖萌,懂的不多")


