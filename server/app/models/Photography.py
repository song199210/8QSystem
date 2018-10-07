from sqlalchemy import Column,Integer,String,Text,DateTime
from app.init_db import Base
from datetime import datetime

class Photography(Base):
    __tablename__="photography"

    id=Column(Integer,primary_key=True)
    title=Column(String(60))
    author=Column(String(40))
    desc=Column(Text)
    imgurlstr=Column(Text)
    content=Column(Text(length=2**32-1))
    isDel=Column(Integer,default=0) #0表示不删除
    cdatetime=Column(DateTime)

    def __init__(self,title,author,desc):
        self.title=title
        self.author=author
        self.desc=desc
        self.cdatetime=datetime.now()

    def __repr__(self):
        return '<Photography %r>' % self.__tablename__

    def to_json(self):
        dict=self.__dict__
        dict['cdatetime']=dict['cdatetime'].strftime("%Y-%m-%d %H:%M:%S")
        if "_sa_instance_state" in dict:
            del dict['_sa_instance_state']
        return dict