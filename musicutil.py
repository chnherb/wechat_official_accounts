#coding=utf8
import urllib2  
from musicutils import xxxutil,yyyutil,zzzutil

def getmusic(keyword):
    try:
        title_artist,album,url = xxxutil.getinfo(keyword)
        if url == None or str(url).strip() == '':
            title_artist,album,url = yyyutil.getinfo(keyword)
        if url == None or str(url).strip() == '':
            title_artist,album,url = zzzutil.getinfo(keyword)
        return title_artist,album,url

    except Exception as e:
        print e
        return '','',None


if __name__ == '__main__':
   
    print(getmusic(u'love'))