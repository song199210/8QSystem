from flask import request,jsonify,Blueprint
from app.controller import common,MusicContro

MusicBlue=Blueprint("MusicBlue",__name__)

@MusicBlue.route("/",methods=['GET'],strict_slashes=False)
def testMusicBlue():
    if request.method == "GET":
        return '<h1>测试访问Music接口成功</h1>'

@MusicBlue.route("/query",methods=['POST'],strict_slashes=False)
def queryMusicJson():
    if request.method == "POST":
        reqJson=common.requestBody(request)
        resJson=MusicContro.queryMusicsM(reqJson)
        return jsonify(resJson)

@MusicBlue.route("/delete",methods=["POST"],strict_slashes=False)
def deleteMusicJson():
    if request.method == "POST":
        reqJson=common.requestBody(request)
        resJson=MusicContro.deleteMusicsM(reqJson)
        return jsonify(resJson)