#-*- coding:utf-8 -*-
import requests
import threadpool
import time
import os,re,random,sys
from urllib import parse
from lxml import etree
from app.model import FilmsM
from app.init_db import session

class ScrapyFilms():
    userAgents=[ #用户代理
        "User-Agent:Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "User-Agent:Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);",
        "User-Agent:Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "User-Agent:Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "User-Agent:Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "User-Agent:Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
        "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
        "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
    ]
    proxy_ip=(
        'http://115.209.116.118:3128',
        'http://118.190.95.35:9001',
        'http://124.234.157.228:80',
        'http://106.75.225.83:808'
    )
    newList=[]
    workThread=None
    page_last=0
    def __init__(self,urlStr,threadNum=1,tag="可播放",page_start=0):
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
            time.sleep(1) #延时0.5s
        pool.wait()
        print("线程结束~~~~~~~~~~~~~~~~~")
        ScrapyFilms.newList.sort()
        print(ScrapyFilms.newList)

    '''开始爬取'''
    def startScrapy(self,url,num):
        urlStr=url.format(self.tag,num)
        headers={
            "user-agent":ScrapyFilms.userAgents[random.randrange(0,len(ScrapyFilms.userAgents))]
        }
        try:
            # url=ScrapyFilms.proxy_ip[random.randrange(0,len(ScrapyFilms.proxy_ip))]
            # proxies_dict={"http":url,"https":url}
            res = requests.get(urlStr, headers=headers)
            resJson = res.json()
            if len(resJson['subjects']) == 0:  # 判断是不是数组并且数据是否为空
                print("抓取结束~~~~~")
            else:
                self.filterData(resJson)
                ScrapyFilms.newList.append(num)
                num = num + 200
                # self.startScrapy(url, num)
        except Exception as err:
            print("Error:{0}—开始抓取".format(err))

    '''爬取详情页面'''
    def scrapyDetail(self,url):
        headers = {
            "user-agent": ScrapyFilms.userAgents[random.randrange(0, len(ScrapyFilms.userAgents))]
        }
        try:
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
            Films=FilmsM(title,fType,director,performer,score,releaseDate,timelen,introduce)
            session.add(Films)
            session.commit()
            return Films.id
        except Exception as err:
            print("Error:{0}—爬取详情出错".format(err))

    '''存储到数据库'''
    def filterData(self,data):
        subjects=data['subjects']
        item=subjects[0]
        id=self.scrapyDetail(item['url'],item['cover'])
        print("id~~~~~~~~:{0}".format(id))
        self.downloadImg_s(item['cover'],id)
        # for item in subjects:
        #     # cover: "https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2181613001.jpg"
        #     # url: "https://movie.douban.com/subject/3552028/"
        #     if item['cover']:
        #         self.downloadImg_s(item['cover'])
        #     if item['url']:
        #         self.scrapyDetail(item['url'])
        # session.add_all(tFilmsData)

    '''将封面图片存储到本地'''
    def downloadImg_s(self,imgcover,id):
        basedir=os.path.dirname(__file__)
        hostpath=parse.urlparse(imgcover)
        imgpathlist=hostpath[2].split("/")
        imgname=imgpathlist[len(imgpathlist) - 1]
        imgpathlist.remove(imgname)
        filepath=os.path.join(basedir,'/'.join(imgpathlist)[1:])
        print(filepath)
        headers = {
            "user-agent": ScrapyFilms.userAgents[random.randrange(0, len(ScrapyFilms.userAgents))]
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
                query=session.query(FilmsM).filter(id==id).all()[0]
            print("图片下载完成~~")
        except Exception as err:
            print("Error:{0}—图片下载出错".format(err))

ScrapyFilmObj=ScrapyFilms('https://movie.douban.com/j/search_subjects?type=movie&tag={0}&sort=rank&page_limit=20&page_start={1}')