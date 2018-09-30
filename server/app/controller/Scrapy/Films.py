#-*- coding:utf-8 -*-
import requests
from requests.exceptions import ProxyError, Timeout
import threadpool
import time
import os,re,random,sys
from urllib import parse
from sqlalchemy.exc import InvalidRequestError
from lxml import etree
from app.init_db import session
from app.controller.Scrapy.config import userAgents
from app.model import FilmsM, ProxyIpM

class ScrapyFilms():
    newList=[]
    workThread=None
    page_last=0
    num1=0 #代理查询的次数
    no_ipproxy=[]
    def __init__(self,urlStr,threadNum=10,page_start=0):
        self.urlStr=urlStr
        self.threadNum=threadNum
        self.page_start=page_start
        self.startThread()

    '''开启线程池'''
    def startThread(self):
        # setlist=[]
        # for num in range(self.threadNum):
        #     setlist.append(((self.urlStr,self.page_start),None))
        #     self.page_start=self.page_start+20
        #
        # pool=threadpool.ThreadPool(self.threadNum) #开启线程池(里面包含len(urllist)线程)
        # requests=threadpool.makeRequests(self.start_scrapy,setlist) #创建任务
        # for req in requests:
        #     pool.putRequest(req)  #将任务放置线程池
        #     time.sleep(1) #延时1~3s
        # pool.wait()
        self.start_scrapy(self.urlStr,self.page_start)

    '''初始化开始爬取'''
    def start_scrapy(self,url,num):
        httpProxy = session.query(ProxyIpM).filter(ProxyIpM.type1 == 'HTTP').all()
        httpsProxy = session.query(ProxyIpM).filter(ProxyIpM.type1 == "HTTPS").all()
        httpData, httpsData = [], []
        if len(httpProxy) != 0:
            for item in httpProxy:
                httpData.append(item.to_json())

        if len(httpsProxy) != 0:
            for item in httpsProxy:
                httpsData.append(item.to_json())
        ScrapyFilms.httpData = httpData
        ScrapyFilms.httpsData = httpsData
        self.getRequest(url,num,self.randipproxy()) #开始请求

    '''设置请求'''
    def getRequest(self,url,num, proxies):
        time.sleep(random.randrange(1,3))
        urlStr=url.format(num)
        print(proxies)
        headers = {
            "user-agent": userAgents[random.randrange(0, len(userAgents))]
        }
        ScrapyFilms.num1 = ScrapyFilms.num1 + 1
        if ScrapyFilms.num1 > 40:
            print("链接超过40次")
            return False
        if proxies in ScrapyFilms.no_ipproxy:
            proxies=self.randipproxy()

        try:
            req = requests.get(urlStr, headers=headers, proxies=proxies,timeout=2)
            print("抓取成功3")
            resJson=req.json()
            print(resJson)
            if len(resJson['subjects']) == 0:  # 判断是不是数组并且数据是否为空
                print("抓取结束~~~~~")
            else:
                self.saveMysql(resJson,proxies)
                num = num + 20
                self.getRequest(url, num, proxies)
        except ProxyError:
            ScrapyFilms.no_ipproxy.append(proxies)
            self.getRequest(url, num,self.randipproxy())
        except Timeout:
            self.getRequest(url, num,self.randipproxy())
        except Exception as err:
            self.getRequest(url, num,self.randipproxy())

    '''设置代理IP'''
    def randipproxy(self):
        proxies = {}
        httpData, httpsData = ScrapyFilms.httpData, ScrapyFilms.httpsData
        if len(httpsData) != 0 and len(httpsData) != 0:
            rd1 = random.randrange(0, len(httpData))
            rd2 = random.randrange(0, len(httpsData))
            proxies['http'] = "{0}:{1}".format(httpData[rd1]['ip'], httpData[rd1]['port'])
            proxies['https'] = "{0}:{1}".format(httpsData[rd2]['ip'], httpsData[rd2]['port'])
            return proxies

    '''分别抓取图片和详情数据保存数据'''
    def saveMysql(self,data,proxies):
        subjects=data['subjects']
        for item in subjects:
            if item['url']:
                id = self.scrapyDetail(item['url'],proxies)
            if item['cover']:
                self.downloadImg_s(item['cover'],id,proxies)

    '''爬取详情页面并存储到数据库'''
    def scrapyDetail(self,url,proxies):
        headers = {
            "user-agent": userAgents[random.randrange(0, len(userAgents))]
        }
        try:
            urlStr=url+"?tag=热门&from=gaia_video"
            res_html=requests.get(urlStr,headers=headers,proxies=proxies,timeout=2).text
            res_html=res_html.encode("utf-8",'ignore')
            ele=etree.HTML(res_html)
            title=ele.xpath('//span[@property="v:itemreviewed"]/text()')[0]
            fType="/".join(ele.xpath('//span[@property="v:genre"]/text()'))
            director="/".join(ele.xpath('//span[@class="attrs"]/a[@rel="v:directedBy"]/text()'))
            performer="/".join(ele.xpath('//span[@class="actor"]/span[@class="attrs"]/a[@rel="v:starring"]/text()'))
            score="/".join(ele.xpath('//strong[@property="v:average"]/text()'))
            releaseDate=",".join(ele.xpath('//span[@property="v:initialReleaseDate"]/text()'))
            timelen="/".join(ele.xpath('//span[@property="v:runtime"]/text()'))
            introduce=";".join(ele.xpath('//span[@property="v:summary"]/text()'))
            try:
                Films = FilmsM(title, fType, director, performer, score, releaseDate, timelen, introduce)
                session.add(Films)
                session.commit()
                return Films.id
            except InvalidRequestError as err:
                print("InvalidRequestError %r" % repr(err))
                session.rollback()
            except Exception as e:
                print("Exception %r" % repr(e))
                session.rollback()
        except Exception as err:
            print("爬取详情Error:{0}".format(err))

    '''将封面图片存储到本地'''
    def downloadImg_s(self,imgcover,id,proxies):
        basedir=os.path.dirname(__file__)
        hostpath=parse.urlparse(imgcover)
        imgpathlist=hostpath[2].split("/")
        imgname=imgpathlist[len(imgpathlist) - 1]
        imgpathlist.remove(imgname)
        filepath=os.path.join(basedir,'..','..','static','/'.join(imgpathlist)[1:])
        headers = {
            "user-agent": userAgents[random.randrange(0, len(userAgents))]
        }
        if not os.path.exists(filepath):
            print("路径不存在,正在创建路径~~~")
            os.makedirs(filepath)
        try:
            res = requests.get(imgcover, headers=headers,proxies=proxies,timeout=2)
            with open(os.path.join(filepath, imgname), "wb") as fp:
                fp.write(res.content)
                fp.close()
                try:
                    query=session.query(FilmsM).filter(FilmsM.id == id).all()[0]
                    imgurl='/static/{0}/{1}'.format('/'.join(imgpathlist)[1:],imgname)
                    query.fimgurl=imgurl
                    session.commit()
                except InvalidRequestError as err:
                    print("InvalidRequestError %r" % repr(err))
                    session.rollback()
                except Exception as e:
                    print("Exception %r" % repr(e))
                    session.rollback()
        except Exception as err:
            print("图片下载Error:{0}".format(err))

ScrapyFilms('https://movie.douban.com/j/search_subjects?type=movie&tag=可播放&sort=rank&playable=on&page_limit=20&page_start={0}')