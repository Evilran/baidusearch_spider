#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: baidusearch_spider.py
Author: Evi1ran
Date Created: Feb 23, 2022
Description: 百度搜索爬虫，爬取百度搜索结果
"""

# built-in imports

# third-party imports
import json
import re
import time
import random
from urllib.parse import urlencode
from lxml import etree
import requests
from requests.adapters import HTTPAdapter
 
s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))


def get_random_UA():
    ua_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100",
        "Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)",
        "Chrome/76.0.3809.100 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/68.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/68.0",
        "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/68.0",
    ]
    return random.choice(ua_list)

def baidu_search(keyword, pn):
    p = {'wd': keyword}
    res = s.get("http://www.baidu.com/s?" +
                urlencode(p)+("&pn={0}&cl=3&rn=10").format(pn), headers={"User-Agent": get_random_UA()}, timeout=10)
    return res.content


def getList(text, abstract=False):
    arr = []
    em = re.compile(r'<em>')
    tree = etree.HTML(em.sub('', text))
    try:
        title = tree.xpath('/html/body/div/div/div/div/div/h3/a/text()')
        href = tree.xpath('/html/body/div/div/div/div/div/h3/a/@href')
        if len(title) == len(href):
            for i in range(len(title)):
                try:
                    res = s.get(href[i], headers={"User-Agent": get_random_UA()}, timeout=10, allow_redirects=False)
                    if abstract:
                        content = etree.HTML(res.content)
                        description = content.xpath('//meta[@itemprop="description"]/@content')
                    else:
                        description = ""
                    url = res.headers.get('location', href[i])
                except:
                    description = ""
                    url = href[i]
                finally:
                    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
                    element = {"title":title[i], 'url': url, 'description': description, 'time': now }
                    arr.append(element)
    except Exception:
        pass
    return arr


def geturl(keyword, page):
    for pg in range(page):
        pn = pg * 10
        #pn=page*100+1
        html = baidu_search(keyword, pn)
        #content = unicode(html, 'utf-8','ignore')
        arrList = getList(html.decode(), True)
        print("Page {0}: {1}".format(pg + 1, len(arrList)))
        save = open('result.json', 'a+', encoding='utf-8')
        for i in arrList:
            arr = json.dumps(i, ensure_ascii=False)
            save.write(arr + '\n')
        save.close()
       

if __name__ == '__main__':
    geturl('北京 公司 首页', page=10)
