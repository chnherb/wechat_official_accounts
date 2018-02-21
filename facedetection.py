#coding=utf8

import requests
from json import JSONDecoder

import os
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
def getImageInfo(image_url):
    try:
        http_url = "https://xxxxxxxxxxxx"
        key = "***************"
        secret = "************"
        # filepath = abspath + "/b.jpg"

        data = {"api_key": key, 
                "api_secret": secret, 
                "return_landmark": "0",
                "image_url": image_url,
                "return_attributes":"gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity" }
        # files = {"image_file": open(filepath, "rb")}
        # response = requests.post(http_url, data=data, files=files)
        response = requests.post(http_url, data=data)

        req_con = response.content.decode('utf-8')
        req_dict = JSONDecoder().decode(req_con)

        # print(req_dict)
        # print "-----------"

        t_list = []
        t_list.append(u"性别：")
        t_list.append(req_dict["faces"][0]["attributes"]["gender"]["value"].decode('utf-8'))

        t_list.append(u"\n年龄：")
        t_list.append(str(req_dict["faces"][0]["attributes"]["age"]["value"]).decode('utf-8'))
        isGlass = req_dict["faces"][0]["attributes"]["eyestatus"]["left_eye_status"]["normal_glass_eye_close"] + req_dict["faces"][0]["attributes"]["eyestatus"]["left_eye_status"]["normal_glass_eye_open"]
        isnotGlass = req_dict["faces"][0]["attributes"]["eyestatus"]["left_eye_status"]["no_glass_eye_open"] + req_dict["faces"][0]["attributes"]["eyestatus"]["left_eye_status"]["no_glass_eye_close"]
        if isGlass < isnotGlass:
            t_list.append(u"\n眼镜：未戴")
        else:
            t_list.append(u"\n眼镜：已戴")
        t_list.append(u"\n笑容：")
        if req_dict["faces"][0]["attributes"]["smile"]["value"] < 50:
            t_list.append(u"无")
        else:
            t_list.append(u"有")
        # print u"人脸姿势：",req_dict["faces"][0]["attributes"]["headpose"]
        t_list.append(u"\n人种：")
        if req_dict["faces"][0]["attributes"]["ethnicity"]["value"] == "Asian":
            t_list.append("亚洲人")
        elif req_dict["faces"][0]["attributes"]["ethnicity"]["value"] == "White":
            t_list.append("白种人")
        else:
            t_list.append("黑种人")

        t_list.append(u"\n情绪分析：")
        t_list.append(u"\n  平静值：")
        t_list.append(str(req_dict["faces"][0]["attributes"]["emotion"]["neutral"]).decode('utf-8'))
        t_list.append(u"\n  厌恶值：") 
        t_list.append(str(req_dict["faces"][0]["attributes"]["emotion"]["disgust"]).decode('utf-8'))
        t_list.append(u"\n  恐惧值：")
        t_list.append(str(req_dict["faces"][0]["attributes"]["emotion"]["fear"]).decode('utf-8'))
        t_list.append(u"\n  高兴值：")
        t_list.append(str(req_dict["faces"][0]["attributes"]["emotion"]["happiness"]).decode('utf-8'))
        t_list.append(u"\n  伤心值：")
        t_list.append(str(req_dict["faces"][0]["attributes"]["emotion"]["sadness"]).decode('utf-8'))
        t_list.append(u"\n  惊讶值：")
        t_list.append(str(req_dict["faces"][0]["attributes"]["emotion"]["surprise"]).decode('utf-8'))
        t_list.append(u"\n  愤怒值：")
        t_list.append(str(req_dict["faces"][0]["attributes"]["emotion"]["anger"]).decode('utf-8'))
        mystr = ''.join(t_list)
        return mystr
    except Exception as e:
        print e
        return u'识别失败，换张图片试试吧^-^'

if __name__ == '__main__':
    # print getImageInfo("http://jiangsu.china.com.cn/uploadfile/2015/0114/1421221304095989.jpg")
    print getImageInfo("http://mmbiz.qpic.cn/mmbiz_jpg/18uqTFRhC4RDa5SKdcdqJm8V1n4Mp2uQiaZ6n1s9C9EYiapjnbsuFUrKerrTmB5yG4kjyf5YkibgGwLGd6eY1eTibQ/0")
