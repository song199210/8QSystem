from app.model import PhotographyM
from app.init_db import session
from sqlalchemy.exc import InvalidRequestError
import logging
from app.controller.Scrapy import Photography

'''查询摄影列表数据'''
def queryPhotographyM(reqJson):
    pageno=reqJson['pageno']
    pagesize=reqJson['pagesize']
    resJson=dict()
    resJson['flag']="error"
    resJson['msg']="查询失败"
    resJson['data']=[]
    try:
        query=session.query(PhotographyM).limit(pageno).offset(pagesize).all()
        if len(query) != 0:
            resJson['flag']="success"
            resJson['msg']="登录成功"
            data=[]
            for item in query:
                data.append(item.to_json())
            resJson['data']=data
    except InvalidRequestError:
        session.rollback()
        resJson['msg']='InvalidRequestError %r' % repr(InvalidRequestError)
        logging.error('InvalidRequestError %r' % repr(InvalidRequestError))
    except Exception as err:
        session.rollback()
        resJson['msg']='Error %r' % repr(err)
        logging.error('Error %r' % repr(err))

    return resJson

'''删除摄影列表数据'''
def deletePhotographyM(reqJson):
    filmId=reqJson['filmId']
    resJson=dict()
    resJson['flag']="error"
    resJson['msg']="删除失败"
    if filmId == "" and not filmId:
        logging.warn("FilmId warn:FilmId不存在")
        print("FilmId warn:FilmId不存在")
        resJson['msg']="FilmId warn:FilmId不存在"
    else:
        try:
            session.query(PhotographyM).filter(PhotographyM.id == filmId).delete(synchronize_session=False)
            resJson['flag']="success"
            resJson['msg']="删除成功"
        except InvalidRequestError:
            session.rollback()
            resJson['msg']="InvalidRequestError:%r" % repr(InvalidRequestError)
            logging.error("InvalidRequestError:%r" % repr(InvalidRequestError))
        except Exception as err:
            session.rollback()
            resJson['msg']="Error:%r" % repr(err)
            logging.error("Error %r" % repr(err))

        return resJson

'''爬虫爬取数据'''
def scrapyPhotographyM():
    Photography.ScrapyPhotography('http://academy.fengniao.com/list.php?action=getList&class_id=190&sub_classid=967&page={0}&not_in_id=0')