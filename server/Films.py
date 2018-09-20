import requests
import threadpool
import time
import os,re,random,sys
from urllib import parse

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
            time.sleep(0.5) #延时0.5s
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
        resJson=requests.get(urlStr,headers=headers).json()
        if len(resJson['subjects']) == 0: #判断是不是数组并且数据是否为空
            print("抓取结束~~~~~")
        else:
            self.saveMysql(resJson)
            ScrapyFilms.newList.append(num)
            basedir=os.path.dirname(__file__)
            filedir=os.path.join(basedir)
            filePath=os.path.join(filedir,"..","films.txt")
            f=open(filePath,"a")
            f.write("urlstr："+urlStr+"\r\n\r\n"+str(num)+"："+str(resJson)+'\r\n\r\n\r\n')
            num=num+200
            self.startScrapy(url,num)

    '''存储到数据库'''
    def saveMysql(self,data):
        subjects=data['subjects']
        tFilmsData=[]
        for item in subjects:
            # cover: "https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2181613001.jpg"
            # url: "https://movie.douban.com/subject/3552028/"
            if item['cover']:
                self.downloadImg_s(item['cover'])

            # tFilmsData.append(FilmsM(title=item.title,score=rate))
        # session.add_all(tFilmsData)

    '''将封面图片存储到本地'''
    def downloadImg_s(self,imgcover):
        basedir=os.path.dirname(__file__)
        hostpath=parse.urlparse(imgcover)
        imgpathlist=hostpath[2].split("/")
        imgname=imgpathlist[len(imgpathlist) - 1]
        imgpathlist.remove(imgname)
        filepath=os.path.join(basedir,'/'.join(imgpathlist)[1:])
        headers = {
            "user-agent": ScrapyFilms.userAgents[random.randrange(0, len(ScrapyFilms.userAgents))]
        }
        if not os.path.exists(filepath):
            print("路径不存在,正在创建路径~~~")
            print(filepath)
            os.makedirs(filepath)
        print(imgcover)
        res=requests.get(imgcover,headers=headers)
        with open(os.path.join(filepath,imgname),"wb") as fp:
            fp.write(res.content)
            fp.close()
        print("图片下载完成~~")

ScrapyFilmObj=ScrapyFilms('https://movie.douban.com/j/search_subjects?type=movie&tag={0}&sort=rank&page_limit=20&page_start={1}')