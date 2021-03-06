from sqlalchemy import Column,Integer,String,Text,DateTime
from app.init_db import Base
from datetime import datetime
from uuid import uuid4

class MusicModels(Base):
    __tablename__="musics"
    id=Column(Integer,primary_key=True) #音乐ID
    title=Column(String(60)) #音乐标题
    type=Column(String(80)) #音乐类型
    director=Column(String(60)) #演唱者
    timelen=Column(String(40)) #音乐时长
    datetime=Column(DateTime) #爬取时间

    def __init__(self,title,type,director,score,releaseDate,timelen,introduce):
        self.title=title
        self.type=type
        self.director=director
        self.timelen=self.timelen
        self.datetime=datetime.now()

    def __repr__(self):
        return '<FilmModels %r>' % self.__tablename__

    def to_json(self):
        dict=self.__dict__
        if dict['datetime']:
            dict['datetime']=dict['datetime'].strftime("%Y-%m-%d %H:%M:%S")
        if "_sa_instance_state" in dict:
            del dict['_sa_instance_state']
        return dict