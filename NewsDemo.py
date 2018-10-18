#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/16 14:35
# @Author  : zh
# @info     :
# @File    : NewsDemo.py
# @Software: PyCharm
import requests
import json
from lxml import etree
import time,datetime
import csv

header = {
        'UserAgent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) '
                     'Chrome / 69.0 .3497 .100 Safari / 537.36',
        'Cookie': 'ustat=__123.9.207.11_1539671313_0.92483300; genTime=1539671313;SINAGLOBAL=571251404734.694.1539677'
                  '532862; sinaPhotoShareTips=1; TUIJIAN_1=usrmdinst_2;Apache=1747851667048.4036.1539739953282; ULV=153'
                  '9739953285:2:2:2:1747851667048.4036.1539739953282:1539677532864; vt=4; statuid=__123.9.207.11_15397'
                  '40790_0.44155600; statuidsrc=Mozilla%2F5.0+%28Linux%' '3B+Android+6.0%3B+Nexus+5+Build%2FMRA58N%29+'
                  'AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F69.0.3497.100+Mobile+Safari%2F537.36%60123.'
                  '9.207.11%60http%3A%2F%2Ftousu.sina.cn%2Fcomplaint%2Fview%2F17347249694%2F%3Fcre%3Dtianyi%26mod%3D'
                  'wtech%26loc%3D0%26r%3D-1%26doct%3D0%26rfunc%3D69%26tj%3Dnone%26tr%3D73%26vt%3D4%26pos%3D18%60https%'
                  '3A%2F%2Ftech.sina.cn%2F%3Ffrom%3Dwap%60__123.9.207.11_1539740790_0.44155600; historyRecord={"href"'
                  ':"https://tech.sina.cn/","refer":"https://news.sina.com.cn/"}'
    }
class News:
    def __init__(self, url, classes):
        self.url = url
        self.classes = classes


def getHtml(offset, ctime):
    response = requests.get("https://cre.dp.sina.cn/api/v3/get?cateid=2L&cre=tianyi&mod=wspt&merge=3&statics=1&ad="
                            "{%22rotate_count%22:1042,%22page_url%22:%22https%3A%2F%2Fsports.sina.cn%2F%22,%22channel"
                            "%22:%22130043%22,%22platform%22:%22wap%22,%22timestamp%22:1539846754758,%22net%22:null}"
                            + "&action=1&up={0}&down=0&length=12&_={1}"
                            .format(offset, ctime), headers=header)
    # print(response.url)
    return response.text


def jsonstr ():
    now = datetime.datetime.now()
    timspan = int(time.mktime(now.timetuple()))
    i = 0
    newsList = []
    while i < 200/15:
        js = json.loads(getHtml(i, timspan*1000))
        print(i)
        for x in range(len(js['data'])):
            try:
                newsList.append(News(js['data'][x]['url_https'], list(js['data'][x]['classes'].keys())[0]))
            except Exception as ex:
                print(ex)
            # print(js['data'][i]['title'], "-"*5, list(js['data'][i]['classes'].keys())[0])
        i += 1
    data = []
    for news in newsList:
        print("*"*20)
        print(news.url)
        if news.url.find("slide.news.sina") >= 0:
            continue
        if news.url.find("blog.sina.com.cn") >= 0:
            continue
        try:
            response = requests.get(news.url, headers=header)
            da = etree.HTML(response.content.decode('utf-8'))
            te = da.xpath("//div[@id='artibody']")
            if len(te) > 0:
                content = te[0].xpath('string(.)')
            else:
                articlt = da.xpath("//div[@id='article']")
                if len(articlt) > 0:
                    content = articlt[0].xpath('string(.)')
                else:
                    art_box = da.xpath("//article[@class='art_box']")
                    content =art_box[0].xpath('string(.)')

            content = content.replace('\n', '').replace('\t', '')

            data.append([content, news.classes])
        except Exception as ex:
            print(ex)
    with open('data.csv', 'a+', newline='', encoding='utf-8-sig') as f:
        write = csv.writer(f)
        write.writerow(['content', 'title'])
        write.writerows(data)


if __name__ == "__main__":
    jsonstr()
