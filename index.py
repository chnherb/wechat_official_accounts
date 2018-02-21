#coding=utf8
# import sae
import sys
import os
app_root = os.path.dirname(__file__) 
sys.path.insert(0, os.path.join(app_root, 'requests'))
import web
import time

from weixinInterface import WeixinInterface
 
urls = (
	'/', 'Hello',
    '/******','WeixinInterface'
)
 
# app_root = os.path.dirname(__file__)
# templates_root = os.path.join(app_root, 'templates')
# render = web.template.render(templates_root)

# app = web.application(urls, globals()).wsgifunc()        
# application = sae.create_wsgi_app(app)

app = web.application(urls, globals())

class Hello:
	def GET(self):
		web.header("Content-Type","text/plain; charset=utf-8")
		return u'\n\n\n\t感谢您的关注，网站目前在建设当中，敬请期待！'
		

if __name__ == '__main__':
    app.run()