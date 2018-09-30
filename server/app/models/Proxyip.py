from sqlalchemy import Column,Integer,String,DateTime
from sqlalchemy.exc import InvalidRequestError
from app.init_db import Base
import datetime

class ProxyIPModels(Base):
    __tablename__="proxyip"
    id=Column(Integer,primary_key=True)
    ip=Column(String(60))
    port=Column(String(20))
    address=Column(String(40))
    type1=Column(String(20))
    time1=Column(String(20))
    time2=Column(String(60))
    cdatetime=Column(DateTime)
    def __init__(self,ip,port,address,type1,time1,time2):
        self.ip=ip
        self.port=port
        self.address=address
        self.type1=type1
        self.time1=time1
        self.time2=time2
        self.cdatetime=datetime.datetime.now()

    def __repr__(self):
        return '<ProxyIP %r>' % repr(self.__tablename__)

    def to_json(self):
        dict=self.__dict__
        # dict['cdatetime']=dict['cdatetime'].strftime("%Y-%m-%d %H:%M:%S")
        # if "_sa_instance_state" in dict:
        #     del dict['_sa_instance_state']
        return dict