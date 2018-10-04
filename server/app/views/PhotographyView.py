from flask import Blueprint,request,jsonify
from app.controller import common,Photography

queryControl=Photography.queryPhotographyM
deleteControl=Photography.deletePhotographyM
scrapyControl=Photography.scrapyPhotographyM

photographyBlue=Blueprint("photographyBlue",__name__)

@photographyBlue.route("/",methods=['GET'])
def testPhotography():
    if request.method == "GET":
        return '<h1>测试photography成功！</h1>'

@photographyBlue.route("/query",methods=['POST'],strict_slashes=False)
def queryPhotography():
    if request.method == "POST":
        resJson=queryControl(request)
        return jsonify(resJson)

@photographyBlue.route("delete",methods=['POST'],strict_slashes=False)
def deletePhotography():
    if request.method == "POST":
        resJson=deleteControl(request)
        return jsonify(resJson)

@photographyBlue.route("scrapy",methods=['POST'],strict_slashes=False)
def scrapyPhotography():
    if request.method == "POST":
        resJson=scrapyControl(request)
        return jsonify(resJson)