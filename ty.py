#_*_coding:utf8_*_
import random
import os
import csv
from urllib import parse
import requests
from lxml import etree
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
ua_list = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
                    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
]
proxyList = []

class Data:
    def GetList(self):
        return [str(self.comName),str(self.name),str(self.many),str(self.time),str(self.phon),str(self.dress),str(self.status)]
class Proxy:
    def __init__(self,hType,ip,port):
        self.hType = hType
        self.ip = ip
        self.port = port
    def GetDic(self):
        return {str(self.hType):str(self.ip)+":"+str(self.port)} 
class Mysprider:
    def GetProx(self):
        headers = {"User-Agent": ua_list[0]}
        req= requests.get("http://www.xicidaili.com/nt/", headers=headers)
        content = etree.HTML(req.content)
        ip_list = content.xpath('//tr/td[2]')
        port_list = content.xpath('//tr/td[3]')
        type_list = content.xpath('//tr/td[6]')
        global proxyList
        for i in range(len(ip_list)):
            proxyList.append(Proxy(type_list[i].text,ip_list[i].text,port_list[i].text))


    def ReadCookie(self):
        with open(os.getcwd()+"\\cookie.txt") as cookieF:
            return cookieF.readline()


    def GetHtml(self,url):
        self.GetProx()
        headers = {'User-Agent': ua_list[random.randint(0,len(ua_list)-1)]
              ,"cookie":self.ReadCookie()}
        global proxyList
        req = requests.get(url=url,proxies =proxyList[random.randint(0,len(proxyList)-1)].GetDic(),headers =headers)
        return req.content.decode('utf8')


    def StratSpider(self,parm):
        fileName = parm
        dataList = []
        parm = parse.urlencode({'key':parm})
        for i in range(1,11):
            try:
                url ="https://www.qichacha.com/search_index?"+parm+"&ajaxflag=1&p="+str(i)
                print(url)
                html = self.GetHtml(url)
                content = etree.HTML(html)
                tr = content.xpath("//table[@class='m_srchList']/tbody/tr")
                for item in tr:
                    data = Data()
                    data.comName = item.xpath('./td[2]/a')[0].xpath('string(.)')#公司名
                    data.name = item.xpath('./td[2]/p[1]/a')[0].xpath('string(.)')#法人名
                    data.many = item.xpath('./td[2]/p[1]/span[1]')[0].xpath('string(.)')[5:]#注册资金
                    data.time =item.xpath('./td[2]/p[1]/span[2]')[0].xpath('string(.)')[5:]#注册时间
                    data.phon = item.xpath('./td[2]/p[2]/span')[0].xpath('string(.)')[3:]#电话
                    data.dress =item.xpath('./td[2]/p[3]')[0].xpath('string(.)').strip('\n')[3:]#地址
                    data.status = item.xpath('./td[3]/span')[0].xpath('string(.)')#状态
                    dataList.append(data.GetList())
            except Exception as ex:
                print(url+"出错:"+ex)
        with open(os.getcwd()+"\\"+fileName+".csv", 'w',newline="",encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            # 先写入columns_name
            writer.writerow(["公司名", "法人", "注册资金", "注册时间", "电话", "地址", "状态"])
            # 写入多行用writerows
            writer.writerows(dataList)

if __name__ == '__main__':
    kname = input("请输入要搜索的名字:")
    try:
        #Mysprider().GetProx()
        Mysprider().StratSpider(kname)
    except Exception as e:
        print(e)
    input("输入回车退出")
        