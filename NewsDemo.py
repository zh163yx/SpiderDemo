#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/16 14:35
# @Author  : zh
# @info     :
# @File    : NewsDemo.py
# @Software: PyCharm
import requests
from lxml import etree
import json
import time,datetime


def getHtml(ctime,endtime):
    header = {
        'UserAgent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) '
                     'Chrome / 69.0 .3497 .100 Safari / 537.36',
    }
    response = requests.get("https://cre.mix.sina.com.cn/api/v3/get?callback="
                            "cateid=1z&cre=tianyi&mod=pctech&merge=3&statics=1&length=50&up=0&down=0&tm={0}&"
                            "action=1&top_id=93sVT%2C941mC%2C93qe9%2C93s0V%2C9410c%2C94519%2C94Cvs%2C94Am6%2"
                            "C94AZW%2C949ih%2C9490i%2C8xqK9%2C%2C&offset=0&ad=%7B%22rotate_count%22%3A100%2C%22"
                            "platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pctech%22%2C%22page_url%22%3A%22https"
                            "%3A%2F%2Ftech.sina.com.cn%2F%22%2C%22timestamp%22%3A{1}%7D&ctime={0}&_={1}"
                            .format(ctime,endtime), headers=header)
    return response.text


def jsonstr ():
     now = datetime.datetime.now()
     endtime = datetime.datetime.now()-datetime.timedelta(days=3)
     print(endtime)
     while now < endtime:
         timspan = int(time.mktime(now))
         now = now-datetime.timedelta(hours=3)
         timespan2 = int(time.mktime(now))*1000
         js = json.loads(getHtml(timspan, timespan2))
         print(js)
         for i in range(len(js['data'])):
             print(js['data'][i]['title'])


if __name__ == "__main__":
    jsonstr()
