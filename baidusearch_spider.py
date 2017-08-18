# coding=utf8
import urllib2
import string
import urllib
import re
import random

def baidu_search(keyword,pn):
    p= {'wd': keyword}
    res=urllib2.urlopen(("http://www.baidu.com/s?"+urllib.urlencode(p)+"&pn={0}&cl=3&rn=100").format(pn))
    html=res.read()
    return html
def getList(regex,text):
    arr = []
    res = re.findall(regex, text)
    if res:
        for r in res:
            r[1].decode('utf-8')
            arr.append(r)
    return arr

def geturl(keyword):
    for page in range(10):
        pn = page*10 + 1
        #pn=page*100+1
        html = baidu_search(keyword,pn)
        #content = unicode(html, 'utf-8','ignore')
        arrList = getList("none;\">(w+\..*)\/&nbsp;<\/a>.*data-tools='\{\"title\":\"(.*)\",\"url", html)
        #titlearr = getList("data-tools='\{\"title\":\"(.*)\",\"url",html)
        print len(arrList)
        save = open('result.txt', 'a+')
        for one in arrList:
            new = one[1].split('"')
            strs = one[0] + " " + new[0] + "\n"
            save.write(strs)
        #print len(titlearr)
        # save = open('result.txt','a+')
        # for url, name in zip(arrList,titlearr):
        #     newname = name.split('"');
        #     name = newname[0]
        #     strs = url + " " + name + "\n"
        #     save.write(strs)



if __name__=='__main__':
    geturl('XX XX 首页')