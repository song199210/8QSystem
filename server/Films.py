#-*- coding:utf-8 -*-
import requests
import threadpool
import time
import os,re,random,sys
from urllib import parse
from lxml import etree
from app.model import FilmsM
from app.init_db import session
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
class ScrapyFilms():
    def __init__(self):
        self.start_selenium()

    def start_selenium(self):
        browser=webdriver.Chrome()
        browser.get("https://movie.douban.com/explore#!type=movie&tag=可播放&sort=rank&page_limit=20&page_start=0")
        wait=WebDriverWait(browser,20)
        morebtn=wait.until(EC.presence_of_element_located(By.CLASS_NAME,".more"))
        morebtn.click()

ScrapyFilmObj=ScrapyFilms()