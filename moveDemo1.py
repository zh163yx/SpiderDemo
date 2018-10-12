#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/11 15:19
# @Author  : zh
# @info    :爬去猫眼<<悲伤逆流成河>>影评,并进行可视化
# @File    : moveDemo1.py
# @Software: PyCharm
import requests
import csv
from matplotlib import pyplot as plt
import os
from datetime import datetime,timedelta
import json
import pyecharts
from wordcloud import WordCloud


def myspider():
    '''
    获取json数据
    :return:jsonStr
    '''

    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) '
                      'Chrome / 69.0 .3497 .100 Safari / 537.36',
        'Referer': 'http: // m.maoyan.com / movie / 1217236 / comments?_v_ = yes',
        'Host': 'm.maoyan.com'
    }
    offset = 0
    startTime = datetime.now()
    while True:
        if offset >= 1000:
            offset = 0
            startTime = startTime+timedelta(days=-1)
        if startTime < datetime.now()+timedelta(days=-5):
            return
        url = 'http://m.maoyan.com/mmdb/comments/movie/1217236.json?_v_=yes&offset={0}&startTime={1}%2015%3A07%3A45'\
            .format(offset, startTime.strftime('%Y-%m-%d'))
        response_comment = requests.get(url=url, headers=headers)
        jsonData = json.loads(response_comment.text)
        dealJson(jsonData['cmts'])
        offset += 15


def dealJson(jsonData):
    '''
    处理json数据提取需要信息
    :return:list
    '''
    #"startTime": "2018-10-10 15:06:41","content": "看这部电影感觉时间过得挺快的，是部好电影。","cityName": "九江","score": 4.5,"nickName": "刻骨灬迷情",
    dataList =[]
    for one in jsonData:
        time = one['startTime']
        cityName = one['cityName']
        if 'gender' in one:
            gender = one['gender']
        else:
            gender = 0
        content = one['content']
        score = one['score']
        nickName = one['nickName']
        oneList = [time, cityName, content, score, nickName, gender]
        dataList.append(oneList)
    saveData(dataList)


def saveData(dataList):
    '''
    将数据存储到本地文件
    :return:null
    '''
    if not os.path.exists('maoyan.csv'):
        name = ['评论时间', '城市', '内容', '评分', '评论者昵称', '性别']
        dataList.insert(0, name)
    with open('maoyan.csv', 'a+', encoding='utf-8-sig', newline='')as f:
        writer = csv.writer(f)
        writer.writerows(dataList)
    print(len(dataList))


def readData():
    '''
    从csv文件中读取数据
    :return: datalist
    '''
    with open('maoyan.csv', 'r', encoding='utf-8-sig', newline='') as f:
        rows = csv.reader(f)
        time =[]
        cityName = []
        content = ''
        score = []
        name = []
        gender = []
        i = 0
        for row in rows:
            if i != 0:
                time.append(row[0])
                cityName.append(row[1])
                content += row[2]
                score.append(row[3])
                name.append(row[4])
                gender.append(row[5])
            i += 1
        print("一共有{0}条记录".format(i))

        # sex_distribution(gender)
        # city_distribution(cityName)
        mywordCloud(content)

def mywordCloud(text1):
    text1 = text1.replace("悲伤逆流成河", '')
    import jieba
    textcut = jieba.cut(text1)
    string = ' '.join(textcut)
    bg = plt.imread(r'img.png')
    print(bg)
    wc = WordCloud(
        font_path=r'C:\Windows\Fonts\Deng.ttf',
        background_color='white',
        random_state=50,
        width=800,
        height=600,
        mask=bg,
    ).generate_from_text(string)
    plt.imshow(wc)
    plt.show()

def city_distribution(cityData):
    '''
    城市图柱状图
    :param cityData:
    :return:
    '''
    city_Dic ={ }
    for i in cityData:
        if i in city_Dic.keys():
            city_Dic[i] += 1
        else:
            city_Dic[i] = 1
    sorted_Dic = sorted(city_Dic.items(), key=lambda d: d[1], reverse=True)#排序后变成元组
    city_name =[]
    city_num = []
    for i in range(len(sorted_Dic)):
        city_name.append(sorted_Dic[i][0])
        city_num.append(sorted_Dic[i][1])
    bar = pyecharts.Bar("城市", title_text_size=20)
    bar.add('城市统计', city_name, city_num, is_label_show=True, is_datazoom_show=True)
    bar.render()

def sex_distribution(sexData):
    '''
    性别饼图
    :return: null
    '''

    number = []
    number.append(sexData.count('0'))
    number.append(sexData.count('1'))
    number.append(sexData.count('2'))
    attr = ['未知', '男', '女']
    pie = pyecharts.Pie("性别图")
    pie.add("", attr, number,is_label_show=True)
    return pie
if __name__ == "__main__":
    # myspider()
    readData()