from flask import Blueprint,request,jsonify
from app.controller import common,UserContro

UserBlue=Blueprint("UserBlue",__name__)

@UserBlue.route("/",methods=["GET"])
def testLogin():
    if request.method == "GET":
        return "测试成功"

@UserBlue.route("/islogin",methods=['POST'],strict_slashes=False)
def isLoginUser():
    if request.method == "POST":
        reqJson=common.requestBody(request)
        resJson=UserContro.isLogin(reqJson)
        return jsonify(resJson)