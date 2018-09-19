from sqlalchemy import Column,Integer,String,Text
from app.init_db import Base

class MenuModels(Base):
    __tablename__="menus"
    id=Column(Integer,primary_key=True)
    icon=Column(Text)
    name=Column(String(60))
    url=Column(String(60))

    def __init__(self,icon,name,url):
        self.icon=icon
        self.name=name
        self.url=url

    def __repr__(self):
        return '<MenuModels %r>' % self.__tablename__

    def to_json(self):
        dict=self.__dict__
        if "_sa_instance_state" in dict:
            del dict['_sa_instance_state']
        return dict