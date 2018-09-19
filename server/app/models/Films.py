from sqlalchemy import Column,Integer,String,Text,DateTime
from app.init_db import Base
from datetime import datetime
from uuid import uuid4

class FilmModels(Base):
    __tablename__="films"
    id=Column(Integer,primary_key=True) #电影ID
    title=Column(String(60)) #电影标题
    type=Column(String(80)) #电影类型
    director=Column(String(60)) #电影导演
    performer=Column(String(60)) #电影演员
    score=Column(String(20)) #电影评分
    releaseDate=Column(DateTime) #上映时间
    timelen=Column(String(40)) #电影时长
    introduce=Column(Text(length=(2**32)-1)) #电影简介
    datetime=Column(DateTime) #爬取时间

    def __init__(self,title,type,director,score,releaseDate,timelen,introduce):
        self.title=title
        self.type=type
        self.director=director
        self.score=score
        self.releaseDate=releaseDate
        self.timelen=timelen
        self.introduce=introduce
        self.datetime=datetime.now()

    def __repr__(self):
        return '<FilmModels %r>' % self.__tablename__

    def to_json(self):
        dict=self.__dict__
        if dict['datetime']:
            dict[datetime]=dict[datetime].strftime("%Y-%m-%d %H:%M:%S")
        if "_sa_instance_state" in dict:
            del dict['_sa_instance_state']
        return dict