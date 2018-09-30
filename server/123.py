#-*- coding:utf-8 -*-
import requests
from requests.exceptions import ProxyError,Timeout
import threadpool
import time
import os,re,random,sys
from urllib import parse
from lxml import etree
from app.model import FilmsM,ProxyIpM
from app.init_db import session
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import sys,random
class ScrapyFilms():
    httpData,httpsData=[],[]
    num=0
    def __init__(self):
        self.start_scrapy()

    def start_selenium(self):
        browser=webdriver.Chrome()
        browser.get("https://movie.douban.com/explore#!type=movie&tag=可播放&sort=rank&page_limit=20&page_start=0")
        wait=WebDriverWait(browser,20)
        isTrue=True
        morebtn = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "more")))
        while(isTrue):
            try:
                element=browser.find_element(By.CLASS_NAME, "more")
                if element.is_displayed():
                    morebtn.click()
                    time.sleep(random.randrange(2,3))
                else:
                    isTrue=False
                    print("DOM元素隐藏")
            except NoSuchElementException as err:
                isTrue=False
                print("DOM元素不存在")
                print(repr(err))
                browser.quit()
                sys.exit()

    def start_scrapy(self):
        httpProxy=session.query(ProxyIpM).filter(ProxyIpM.type1 == 'HTTP').all()
        httpsProxy=session.query(ProxyIpM).filter(ProxyIpM.type1 == "HTTPS").all()
        httpData,httpsData=[],[]
        ScrapyFilms.num=ScrapyFilms.num+1
        if len(httpProxy) != 0:
            for item in httpProxy:
                httpData.append(item.to_json())

        if len(httpsProxy) != 0:
            for item in httpsProxy:
                httpsData.append(item.to_json())
        ScrapyFilms.httpData=httpData
        ScrapyFilms.httpsData=httpsData
        self.getRequest(self.randipproxy())


    def randipproxy(self):
        proxies = {}
        httpData, httpsData=ScrapyFilms.httpData,ScrapyFilms.httpsData
        if len(httpsData) != 0 and len(httpsData) != 0:
            rd1 = random.randrange(0, len(httpData))
            rd2 = random.randrange(0, len(httpsData))
            proxies['http'] = "{0}:{1}".format(httpData[rd1]['ip'], httpData[rd1]['port'])
            proxies['https'] = "{0}:{1}".format(httpsData[rd2]['ip'], httpsData[rd2]['port'])
            print("~~~~~~~~~~~~~~~~")
            print(proxies)
            return proxies

    def getRequest(self,proxies):
        url="https://movie.douban.com/explore#!type=movie&tag=可播放&sort=rank&page_limit=20&page_start=0"
        headers={
            "user-agent":"User-Agent:Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        ScrapyFilms.num=ScrapyFilms.num+1
        if ScrapyFilms.num > 20:
            print("链接超过20次")
            return False

        try:
            req = requests.get(url, headers=headers, proxies=proxies)
            print(req.text)
        except ProxyError:
            print("代理报错~~~~~~~~~~~~~")
            self.getRequest(self.randipproxy())
        except Timeout:
            print("链接超时~~~~~~~~~~~~")
            self.getRequest(self.randipproxy())
        except Exception as err:
            print("未知错误")

ScrapyFilmObj=ScrapyFilms()