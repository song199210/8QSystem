from flask import request,jsonify,Blueprint
from app.controller import common,JokeContro

JokeBlue=Blueprint("JokeBlue",__name__)

@JokeBlue.route("/",methods=['GET'],strict_slashes=False)
def testJokeBlue():
    if request.method == "GET":
        return "<h1>测试访问Joke接口成功</h1>"

'''查询推荐笑话数据列表'''
@JokeBlue.route("/query",methods=['POST'],strict_slashes=False)
def queryJokeJson():
    if request.method == "POST":
        reqJson=common.requestBody(request)
        resJson=JokeContro.queryJokesM(reqJson)
        return jsonify(resJson)

'''删除推荐笑话数据列表'''
@JokeBlue.route("delete",methods=['POST'],strict_slashes=False)
def deleteJokeJson():
    if request.method == "POST":
        reqJson=common.requestBody(request)
        resJson=JokeContro.deleteJokesM(reqJson)
        return jsonify(resJson)