from sqlalchemy import Column,Integer,String,Text,DateTime
from app.init_db import Base
from uuid import uuid4
from datetime import datetime

class JokeModels(Base):
    __tablename__="jokes"
    id=Column(Integer,primary_key=True)
    title=Column(String(60)) #笑话ID
    contect=Column(Text) #笑话内容
    views=Column(Integer,default=0)   #浏览次数
    datetime=Column(DateTime) #爬取时间
    def __init__(self,title,contect,views):
        self.title=title
        self.contect=contect
        self.views=views
        self.datetime=datetime.now()
    def __repr__(self):
        return '<JokeModels %r>' % self.__tablename__

    def to_json(self):
        dict = self.__dict__
        if dict['datetime']:
            dict[datetime] = dict[datetime].strftime("%Y-%m-%d %H:%M:%S")
        if "_sa_instance_state" in dict:
            del dict['_sa_instance_state']
        return dict