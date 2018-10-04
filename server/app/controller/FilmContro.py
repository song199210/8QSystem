from app.model import FilmsM
from app.init_db import session
from sqlalchemy import func
from sqlalchemy.exc import InvalidRequestError
import logging
from app.controller.Scrapy import Films

'''查询电影列表数据'''
def queryFilmsM(reqJson):
    pageno=reqJson['pageno']
    pagesize=reqJson['pagesize']
    resJson=dict()
    resJson['flag']="error"
    resJson['msg']="查询失败"
    resJson['data']=[]
    try:
        offsetnum=pagesize*(pageno-1)
        total=session.query(func.count(FilmsM.id)).scalar()
        if offsetnum < total:
            query=session.query(FilmsM.id,FilmsM.title,FilmsM.type,FilmsM.score,FilmsM.fimgurl).limit(pagesize).offset(offsetnum).all()
            resJson['flag'] = "success"
            resJson['msg'] = "查询成功"
            if len(query) != 0:
                data=[]
                for item in query:
                    obj={
                        "id":item[0],
                        "title":item[1],
                        "type":item[2],
                        "score":item[3],
                        "fimgurl":item[4]
                    }
                    data.append(obj)
                resJson['data']=data
        else:
            resJson['flag'] = "success"
            resJson['msg'] = "查询成功"
            resJson['data'] = []
            
    except InvalidRequestError:
        session.rollback()
        resJson['msg']='InvalidRequestError %r' % repr(InvalidRequestError)
        logging.error('InvalidRequestError %r' % repr(InvalidRequestError))
    except Exception as err:
        session.rollback()
        resJson['msg']='Error %r' % repr(err)
        logging.error('Error %r' % repr(err))

    return resJson

'''查看电影详情'''
def lookDetailFilmsM(reqJson):
    filmId=reqJson['filmId']
    resJson={}
    resJson['flag']="error"
    resJson['msg']="查询失败"
    if filmId == "" and not filmId:
        logging.warn("FilmId warn:FilmId不存在")
        print("FilmId warn:FilmId不存在")
        resJson['msg']="FilmId warn:FilmId不存在"
    else:
        try:
            detailFilms=session.query(FilmsM).filter(FilmsM.id == filmId).all()
            resJson['flag']="success"
            resJson['msg']="查询成功"
            if len(detailFilms) != 0:
                resJson['data']=detailFilms[0].to_json()
        except InvalidRequestError:
            session.rollback()
            resJson['msg']="InvalidRequestError:%r" % repr(InvalidRequestError)
            logging.error("InvalidRequestError:%r" % repr(InvalidRequestError))
        except Exception as err:
            session.rollback()
            resJson['msg']="Error:%r" % repr(err)
            logging.error("Error %r" % repr(err))

        return resJson

'''删除电影列表数据'''
def deleteFilmsM(reqJson):
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
            session.query(FilmsM).filter(FilmsM.id == filmId).delete(synchronize_session=False)
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
def scrapyFilmsM():
    Films.ScrapyFilms('https://movie.douban.com/j/search_subjects?type=movie&tag={0}&sort=rank&page_limit=20&page_start={1}')