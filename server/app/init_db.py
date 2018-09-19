from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

connect=create_engine("mysql://root:root1234@localhost:3306/8Q_db?charset=utf8&autocommit=true",
                        convert_unicode=True, encoding="utf8", echo=True)  # 创建数据库连接引擎
session_class=sessionmaker(bind=connect)
session=session_class()
Base=declarative_base()

def init_db():
    Base.metadata.create_all(connect)

def drop_db():
    Base.metadata.drop_all(connect)