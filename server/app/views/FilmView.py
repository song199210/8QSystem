from flask import request,jsonify,Blueprint
from app.controller import common,FilmContro

FilmBlue=Blueprint("fileBlue",__name__)

@FilmBlue.route("/",methods=['GET'],strict_slashes=False)
def testFilmBlue():
    if request.method == "GET":
        return "<h1>测试访问Film接口成功</h1>"

'''查询推荐电影数据列表'''
@FilmBlue.route("/query",methods=['POST'],strict_slashes=False)
def queryFilmJson():
    if request.method == "POST":
        reqJson=common.requestBody(request)
        resJson=FilmContro.queryFilmsM(reqJson)
        return jsonify(resJson)

'''删除推荐电影的列表数据'''
@FilmBlue.route("/delete",methods=['POST'],strict_slashes=False)
def deleteFilmJson():
    if request.method == "POST":
        reqJson=common.requestBody(request)
        resJson=FilmContro.deleteFilmsM(reqJson)
        return jsonify(resJson)