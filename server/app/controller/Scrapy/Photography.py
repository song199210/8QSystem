import requests
from requests.exceptions import RequestException,Timeout,ProxyError
from sqlalchemy.exc import InvalidRequestError
from lxml import etree
from app.model import PhotographyM
from app.init_db import session
from .config import userAgents
import time,os,random
from .common import Proxies
from urllib import parse
import json
s=requests.session()
s.keep_alive=False
class ScrapyPhotography(Proxies):
    num1=0 #设置请求次数限制
    def __init__(self,url):
        super().__init__()
        self.start_scrapy(url)

    def start_scrapy(self,url):
        self.getProxy()
        self.getRequest(url,2,self.randipproxy())

    def getRequest(self,url,num,proxies):
        print(proxies)
        time.sleep(random.randrange(1,4))
        urlStr=url.format(num)
        print(urlStr)
        headers={
            'Connection': 'close',
            "user-agent":userAgents[random.randrange(0,len(userAgents))]
        }
        if ScrapyPhotography.num1 > 40:
            print("请求超过40次,请稍后再次请求!")
            return False
        if proxies in self.no_ipproxy:
            proxies=self.randipproxy()

        try:
            req=s.get(urlStr,headers=headers,proxies=proxies,timeout=2)
            resJson=req.json()
            print("~~~~~~~~~~~~~~~~~~~~~~~")
            print(resJson)
            data_list=resJson['data']
            if resJson['status'] == 1 and len(data_list) != 0:
                for item in data_list:
                    title=item['title']
                    author=item['author']
                    desc=item['content']
                    imgurl=item['pic_url']
                    src_str=parse.urlparse(imgurl)[2]
                    print(src_str)
                    print("slide" in item['url'])
                    if "slide" in item['url']:
                        continue
                    else:
                        idStr=self.saveMysql(title,author,desc)
                        self.savePic(imgurl,proxies,idStr)
                        self.scrapyDetail(item['url'],proxies,idStr)
                num=num+1
                self.getRequest(url,num,proxies)
            else:
                return False

        except ProxyError:
            print("代理Error: %r" % ProxyError)
            ScrapyPhotography.num1+=1
            self.no_ipproxy.append(proxies)
            self.getRequest(url,num,self.randipproxy())
        except Timeout:
            print("超时Error: %r" % Timeout)
            ScrapyPhotography.num1+=1
            self.no_ipproxy.append(proxies)
            self.getRequest(url,num,self.randipproxy())
        except Exception as err:
            print("未知Error: %r" % err)
            ScrapyPhotography.num1+=1
            self.no_ipproxy.append(proxies)
            self.getRequest(url,num,self.randipproxy())

    def scrapyDetail(self,detailurl,proxies,id):
        headers={
            'Connection': 'close',
            "user-agent":userAgents[random.randrange(0,len(userAgents))]
        }
        req=s.get(detailurl,headers=headers,proxies=proxies,timeout=2)
        htmlStr=req.text
        ele=etree.HTML(htmlStr)
        content_ele=ele.xpath("//div[@class='txt-wrap']")[0]
        content_str=etree.tostring(content_ele,encoding="utf-8",method="HTML",pretty_print=True)
        print(content_str)
        try:
            Photography = session.query(PhotographyM).filter(PhotographyM.id == id).all()
            if len(Photography) != 0:
                Photography[0].content=content_str
                session.commit()
        except InvalidRequestError:
            print("更新Error: %r" % InvalidRequestError)
            session.rollback()
        except Exception as err:
            print("Mysql2未知Error: %r" % err)
            session.rollback()


    def savePic(self,imgcover,proxies,id):
        basedir=os.path.dirname(__file__)
        hostpath=parse.urlparse(imgcover)
        imgpathlist=hostpath[2].split("/")
        imgname=imgpathlist[len(imgpathlist)-1]
        imgpathlist.remove(imgname)
        print("path~~~~~~~~~~~~~~~~~~~")
        imgpath=os.path.abspath(os.path.join(basedir,'..','..','static','phtography',"/".join(imgpathlist)[1:]))
        headers={
            'Connection': 'close',
            "user-agent":userAgents[random.randrange(0,len(userAgents))]
        }
        if not os.path.exists(imgpath):
            print("路径不存在,正在创建路径~~~~~~")
            os.makedirs(imgpath)
        try:
            res=s.get(imgcover,headers=headers,proxies=proxies,timeout=2)
            with open(os.path.join(imgpath,imgname),"wb") as fp:
                fp.write(res.content)
                fp.close()
                try:
                    query=session.query(PhotographyM).filter(PhotographyM.id==id).all()[0]
                    imgurl='/static/photography/{0}/{1}'.format("/".join(imgpathlist)[1:],imgname)
                    query.imgurlstr=imgurl
                    session.commit()
                except InvalidRequestError as err:
                    print("InvalidRequestError %r" % repr(err))
                    session.rollback()
                except Exception as e:
                    print("Exception %r" % repr(e))
                    session.rollback()
        except Exception as err:
            print("图片下载Error:{0}".format(err))

    def saveMysql(self,title,author,desc):
        try:
            insert_sql = PhotographyM(title,author,desc)
            session.add(insert_sql)
            session.commit()
            return insert_sql.id
        except InvalidRequestError:
            print("插入Error: %r" % InvalidRequestError)
            session.rollback()
        except Exception as err:
            print("Mysql3未知Error: %r" % err)
            session.rollback()

