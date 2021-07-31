#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: baidusearch_spider.py
Author: Evi1ran
Date Created: Jul 31, 2021
Description: 百度搜索爬虫，爬取百度搜索结果
"""

# built-in imports

# third-party imports
import re
from urllib.parse import urlencode
from lxml import etree
import requests
from requests.adapters import HTTPAdapter
 
s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))

def baidu_search(keyword, pn):
    p = {'wd': keyword}
    res = s.get("http://www.baidu.com/s?" +
                           urlencode(p)+("&pn={0}&cl=3&rn=10").format(pn), timeout=10)
    return res.content


def getList(text):
    arr = []
    em = re.compile(r'<em>')
    tree = etree.HTML(em.sub('', text))
    try:
        title = tree.xpath('/html/body/div/div/div/div/div/h3/a/text()')
        href = tree.xpath('/html/body/div/div/div/div/div/h3/a/@href')
        if len(title) == len(href):
            for i in range(len(title)):
                try:
                    res = s.get(href[i], timeout=10, allow_redirects=False)
                    arr.append(res.headers.get(
                        'location', href[i]) + ' ' + title[i])
                except:
                    arr.append(href[i] + ' ' + title[i])
    except Exception:
        pass
    return arr


def geturl(keyword, page):
    for pg in range(page):
        pn = pg * 10 + 1
        #pn=page*100+1
        html = baidu_search(keyword, pn)
        #content = unicode(html, 'utf-8','ignore')
        arrList = getList(html.decode())
        print("Page {0}: {1}".format(pg + 1, len(arrList)))
        save = open('result.txt', 'a+', encoding='utf-8')
        save.write('\n'.join(arrList))
        save.close()
       

if __name__ == '__main__':
    geturl('北京 公司 首页', page=10)
