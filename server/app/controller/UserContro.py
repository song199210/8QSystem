from app.model import UsersM,MenusM
from app.init_db import session
from sqlalchemy import and_
from sqlalchemy.exc import InvalidRequestError
import logging

'''判断是否登录成功'''
def isLogin(reqJson):
    uname=reqJson['uname']
    pwd=reqJson['pwd']
    resJson=dict()
    resJson['flag'] = "error"
    resJson['msg'] = "登录失败"
    resJson['data']={}
    try:
        query = session.query(UsersM).filter(and_(UsersM.uname == uname, UsersM.pwd == pwd)).all()
        if len(query) != 0:
            resJson['flag']="success"
            resJson['msg']="登录成功"
            q_menu=session.query(MenusM).all()
            if len(q_menu) != 0:
                data=[]
                for item in q_menu:
                    data.append(item.to_json())
                resJson['data']={"menus":data}

    except InvalidRequestError:
        session.rollback()
        resJson['msg']="InvalidRequestError:%r" % repr(InvalidRequestError)
        logging.error("InvalidRequestError:%r" % repr(InvalidRequestError))
    except Exception as err:
        session.rollback()
        resJson['msg']="Exception:%r" % repr(Exception)
        logging.error("Exception:%r" % repr(Exception))
    return resJson