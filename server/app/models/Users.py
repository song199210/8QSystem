from sqlalchemy import Column,Integer,String,DateTime
from app.init_db import Base
from uuid import uuid4
from datetime import datetime

class UserModels(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    uname=Column(String(60),unique=True)
    pwd=Column(String(60))
    uuid=Column(String(100),unique=True)
    datetime=Column(DateTime)

    def __init__(self,uname,pwd):
        self.uname=uname
        self.pwd=pwd
        self.datetime=datetime.now()
        self.uuid=uuid4()

    def __repr__(self):
        return '<Users %r>' % self.__tablename__

    def to_json(self):
        dict=self.__dict__
        if dict['datetime']:
            dict[datetime]=dict[datetime].strftime("%Y-%m-%d %H:%M:%S")
        if "_sa_instance_state" in dict:
            del dict['_sa_instance_state']
        return dict