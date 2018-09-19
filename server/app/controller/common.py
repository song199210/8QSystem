#-*-coding:utf-8-*-
import json

#获取GET或POST请求参数
def requestBody(request):
    try:
        cType=request.headers['Content-Type']
        if cType == "application/x-www-form-urlencoded; charset=UTF-8":
            return request.values
        elif cType == "multipart/form-data":
            return request.form
        elif cType == "text/plain;charset=UTF-8":
            return json.loads(str(request.data,encoding="utf-8"))
        else:
            return request.values
    except:
        return request.values
