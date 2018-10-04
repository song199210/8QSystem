import random
from app.init_db import session
from app.model import ProxyIpM
class Proxies():
    httpProxy,httpsProxy=[],[]

    def __init__(self):
        self.no_ipproxy=[]  #设置ip白名单

    '''获取代理IP'''
    def getProxy(self):
        httpProxy = session.query(ProxyIpM).filter(ProxyIpM.type1 == 'HTTP').all()
        httpsProxy = session.query(ProxyIpM).filter(ProxyIpM.type1 == "HTTPS").all()
        httpData, httpsData = [], []
        if len(httpProxy) != 0:
            for item in httpProxy:
                httpData.append(item.to_json())

        if len(httpsProxy) != 0:
            for item in httpsProxy:
                httpsData.append(item.to_json())
        Proxies.httpData = httpData
        Proxies.httpsData = httpsData

    '''设置随机IP代理'''
    def randipproxy(self):
        proxies = {}
        httpData, httpsData = Proxies.httpData, Proxies.httpsData
        if len(httpsData) != 0 and len(httpsData) != 0:
            rd1 = random.randrange(0, len(httpData))
            rd2 = random.randrange(0, len(httpsData))
            proxies['http'] = "{0}:{1}".format(httpData[rd1]['ip'], httpData[rd1]['port'])
            proxies['https'] = "{0}:{1}".format(httpsData[rd2]['ip'], httpsData[rd2]['port'])
            return proxies