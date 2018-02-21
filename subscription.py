#!/usr/bin/python
#coding=utf8

'''
通过搜狗搜索中的微信搜索入口来爬取
author:Huangbo
email:chnhuangbo@gmail.com
date:2017-09-23
'''

#这三行代码是防止在python2上面编码错误的，在python3上面不要要这样设置
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from urllib import quote
from pyquery import PyQuery as pq

import requests
import time
import re
import json
import os
abspath = os.path.dirname(sys.argv[0])   
if not os.path.isdir(abspath):
    abspath = sys.path[0]
if not os.path.isdir(abspath):
    abspath = os.path.dirname(__file__)
os.chdir(abspath)

class Subscription:

	def __init__(self, keywords):
		' 构造函数 '
		self.keywords = keywords
		# 搜狐微信搜索链接入口
		# self.sogou_search_url = 'http://weixin.sogou.com/weixin?type=1&query=%s&ie=utf8&s_from=input&_sug_=n&_sug_type_=' % quote(self.keywords)
		if isinstance(self.keywords,unicode):
			self.keywords = quote(str(self.keywords))
		self.sogou_search_url = 'http://weixin.sogou.com/weixin?type=2&query=%s&ie=utf8&s_from=input&_sug_=y&_sug_type_=' % self.keywords
								
		# 爬虫伪装头部设置
		self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
		# 设置操作超时时长
		self.timeout = 5
		# 爬虫模拟在一个request.session中完成
		self.s = requests.Session()
		
	
	#搜索入口地址，以公众为关键字搜索该公众号	
	def get_search_result_by_keywords(self):
		return self.s.get(self.sogou_search_url, headers=self.headers, timeout=self.timeout).content
	
	
	#获取公众号文章内容
	def parse_wx_articles_by_html(self, selenium_html):
		try:
			doc = pq(selenium_html)
			ul = doc('ul[class="news-list"]')
			# ul = doc('ul')
			list_article = []
			for index,li in enumerate(ul('li').items()):
				d = dict()
				div_imgbox = li('div[class="img-box"]')
				imgs = []
				if div_imgbox.html() is None:
					div_imgbox = li('div[class="img-d"]')
				for img in div_imgbox('img').items():
					imgs.append(img.attr('src'))
				d["imgs"] = imgs	

				div_txtbox = li('div[class="txt-box"]')
				title = div_txtbox('h3').text()
				d["title"] = title
				url = div_txtbox('a').attr('href')
				d["url"] = url
				description = div_txtbox('p[class="txt-info"]').text()
				d["description"] = description
				account = div_txtbox('a[class="account"]').text()
				d["account"] = account
				list_article.append(d)
				if index == 5:
					break
			# return json.dumps(list_article)
			return list_article
		
		except Exception as e:
			# print e
			return ""


	#创建公众号命名的文件夹
	def create_dir(self):
		if not os.path.exists(self.keywords):  
			os.makedirs(self.keywords) 
			
	#爬虫主函数
	def getInfo(self):
		' 爬虫入口函数 '
		#Step 0 ：  创建公众号命名的文件夹
		# self.create_dir()
		
		# Step 1：GET请求到搜狗微信引擎，以微信公众号英文名称作为查询关键字
		sougou_search_html = self.get_search_result_by_keywords()

		# with open(str(self.keywords) + '/' + str(self.keywords) + '.html', 'w') as fr:
		# 	fr.write(sougou_search_html)
		
		return self.parse_wx_articles_by_html(sougou_search_html)

def getResponseImageTextXml(FromUserName, ToUserName, list_article):
	"""
		source = [title, description, picurl, url]
	"""
	itemXml = []
	for article in list_article:
		# source = [title1, description1, picurl, url]
		singleXml = """
			<item>
				<Title><![CDATA[%s]]></Title>
				<Description><![CDATA[%s]]></Description>
				<PicUrl><![CDATA[%s]]></PicUrl>
				<Url><![CDATA[%s]]></Url>
			</item>
		""" % (article["title"], article["description"], article["imgs"][0], article["url"])
		itemXml.append(singleXml)
	reply = """
		<xml>
			<ToUserName><![CDATA[%s]]></ToUserName>
			<FromUserName><![CDATA[%s]]></FromUserName>
			<CreateTime>%s</CreateTime>
			<MsgType><![CDATA[news]]></MsgType>
			<ArticleCount>%d</ArticleCount>
			<Articles>
				%s
			</Articles>
		</xml>
	""" % (FromUserName, ToUserName, str(int(time.time())), len(list_article), " ".join(itemXml))
	# response = make_response(reply)
	# response.content_type = 'application/xml'
	# return response
	# print(reply)
	return reply

def getInfo(FromUserName, ToUserName, keywords):
	return getResponseImageTextXml(FromUserName, ToUserName, Subscription(keywords).getInfo())

if __name__ == '__main__':
	info = getInfo("sfjk", "bbb",u"ios")

	
