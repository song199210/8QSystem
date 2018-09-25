#-*- coding:utf-8 -*-
import requests
import threadpool
import time
import os,re,random,sys
from urllib import parse
from sqlalchemy.exc import InvalidRequestError
from lxml import etree
from app.model import FilmsM
from app.init_db import session
from .config import userAgents,proxy_ip

class ScrapyFilms():
    newList=[]
    workThread=None
    page_last=0
    def __init__(self,urlStr,threadNum=10,tag="可播放",page_start=0):
        self.urlStr=urlStr
        self.threadNum=threadNum
        self.tag=tag
        self.page_start=page_start
        self.startThread()


    '''开启线程池'''
    def startThread(self):
        setlist=[]
        for num in range(self.threadNum):
            setlist.append(((self.urlStr,self.page_start),None))
            self.page_start=self.page_start+20

        pool=threadpool.ThreadPool(self.threadNum) #开启线程池(里面包含len(urllist)线程)
        requests=threadpool.makeRequests(self.startScrapy,setlist) #创建任务
        for req in requests:
            pool.putRequest(req)  #将任务放置线程池
            time.sleep(3) #延时0.5s
        pool.wait()
        print("线程结束~~~~~~~~~~~~~~~~~")
        ScrapyFilms.newList.sort()

    '''开始爬取'''
    def startScrapy(self,url,num):
        urlStr=url.format(self.tag,num)
        headers={
            "user-agent":userAgents[random.randrange(0,len(userAgents))]
        }
        try:
            # url=ScrapyFilms.proxy_ip[random.randrange(0,len(ScrapyFilms.proxy_ip))]
            # proxies_dict={"http":url,"https":url}
            res = requests.get(urlStr, headers=headers)
            resJson = res.json()
            if len(resJson['subjects']) == 0:  # 判断是不是数组并且数据是否为空
                print("抓取结束~~~~~")
            else:
                self.saveMysql(resJson)
                ScrapyFilms.newList.append(num)
                num = num + 200
                self.startScrapy(url, num)
        except Exception as err:
            print("Error:{0}—开始抓取".format(err))

    '''爬取详情页面并存储到数据库'''
    def scrapyDetail(self,url):
        headers = {
            "user-agent": userAgents[random.randrange(0, len(userAgents))]
        }
        try:
            print(url)
            print("开启调试")
            urlStr=url+"?tag=热门&from=gaia_video"
            res_html=requests.get(urlStr,headers=headers).text
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
            print("Error:{0}—爬取详情出错".format(err))

    ''''''
    def saveMysql(self,data):
        subjects=data['subjects']
        item=subjects[0]
        time.sleep(1)
        id=self.scrapyDetail(item['url'])
        time.sleep(1)
        self.downloadImg_s(item['cover'],id)
        for item in subjects:
            if item['cover']:
                self.downloadImg_s(item['cover'])
            if item['url']:
                self.scrapyDetail(item['url'])

    '''将封面图片存储到本地'''
    def downloadImg_s(self,imgcover,id):
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
            print(filepath)
            os.makedirs(filepath)
        try:
            res = requests.get(imgcover, headers=headers)
            with open(os.path.join(filepath, imgname), "wb") as fp:
                fp.write(res.content)
                fp.close()
                try:
                    query=session.query(FilmsM).filter(FilmsM.id == id).all()[0]
                    imgurl='http://localhost:5000/static/{0}/{1}'.format('/'.join(imgpathlist)[1:],imgname)
                    query.fimgurl=imgurl
                    session.commit()
                except InvalidRequestError as err:
                    print("InvalidRequestError %r" % repr(err))
                    session.rollback()
                except Exception as e:
                    print("Exception %r" % repr(e))
                    session.rollback()
        except Exception as err:
            print("Error:{0}—图片下载出错".format(err))
