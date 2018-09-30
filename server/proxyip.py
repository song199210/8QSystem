import requests
from requests.exceptions import ConnectionError
from lxml import etree
from app.init_db import session
from app.model import ProxyIpM
import time

def startProxyIP(url):
    headers={
        "user-agent":"User-Agent:Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    }
    try:
        req = requests.get(url, headers=headers)
        restext = req.text
        ele=etree.HTML(restext)
        tr_dom_list=ele.xpath("//table[@id='ip_list']//tr")
        for index in range(len(tr_dom_list)):
            tr_item=tr_dom_list[index]
            if index != 0:
                td_dom_list=tr_item.xpath("./td[not(@class)]")
                if len(td_dom_list) != 0:
                    ipStr=td_dom_list[0].xpath('./text()')[0]
                    port=td_dom_list[1].xpath("./text()")[0]
                    address=td_dom_list[2].xpath("./a/text()")[0]
                    type1=td_dom_list[3].xpath("./text()")[0]
                    time1=td_dom_list[4].xpath("./text()")[0]
                    time2=td_dom_list[5].xpath("./text()")[0]
                    proxyip=ProxyIpM(ipStr,port,address,type1,time1,time2)
                    session.add(proxyip)
                    session.commit()

    except ConnectionError:
        print(repr(ConnectionError))

startProxyIP("http://www.xicidaili.com/nn")