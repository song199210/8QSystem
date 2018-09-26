# -*- coding:utf-8 -*-
import requests
import threadpool
import time
import os, re, random, sys
from urllib import parse
from sqlalchemy.exc import InvalidRequestError
from lxml import etree
from selenium import webdriver
from app.model import FilmsM
from app.init_db import session


class ScrapyFilms():
    newList = []
    workThread = None
    page_last = 0
    client = None  # selenium框架初始化客户端

    def __init__(self, tag="可播放", page_start=0):
        self.tag = tag
        self.page_start = page_start
        # self.startThread()
        self.initSelenium()

    '''初始化selenium框架'''

    def initSelenium(self):
        browser = webdriver.Chrome()
        browser.get("https://www.baidu.com")

scrapyObj=ScrapyFilms()