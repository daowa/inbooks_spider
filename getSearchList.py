
# coding: utf-8

# In[ ]:


import urllib2
from bs4 import BeautifulSoup, element, Comment
import time
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# In[ ]:

import MySQLdb
conn=MySQLdb.connect(host='localhost',user='inbook',passwd='abcd@123',db='inbook',port=3306,charset='utf8')


# In[ ]:

def requestSoup(url):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    content = response.read()
    soup = BeautifulSoup(content, 'lxml')
    return soup


# In[ ]:

def searchBaiKe(word, count):
    # 抓取网页
    soup = requestSoup("https://baike.baidu.com/search?word=" + word + "&pn=0&rn=0&enc=utf8")
    # 结构化处理
    this_search_list = []
    for result in soup.find_all(class_='result-title', limit=count):
        search = {} #第一遍遍历结果的时候将search初始化
        search['title'] = "".join([item.string for item in result.contents])
        search['from_'] = 'baidubaike'
        search['url'] = result['href']
        search['image'] = ''
        search['time'] = time.time()
        this_search_list.append(search)
    for index, result in enumerate(soup.find_all(class_='result-summary', limit=count)):
        this_search_list[index]['introduce'] = "".join([item.string for item in result.contents])
    return this_search_list


# In[ ]:

def searchDouBan(word, count):
    # 抓取网页
    soup = requestSoup("https://book.douban.com/subject_search?search_text=" + word + "&cat=1001")
    # 结构化处理
    this_search_list = []
    for result in soup.find_all(class_='subject-item', limit=count):
        search = {} #第一遍遍历结果的时候将search初始化
        search['title'] = result.find_all('a')[1]['title']
        try:
            search['introduce'] = (result.find(class_='pub').string.strip().replace('/', '')).decode('utf8')
        except:
            search['introduce'] = ''
        search['from_'] = 'doubandushu'
        search['url'] = result.find_all('a')[1]['href']
        search['image'] = result.find('img')['src']
        search['time'] = time.time()
        this_search_list.append(search)
    return this_search_list


# In[ ]:

def searchGongZhongHao(word, count):
    # 抓取网页
    soup = requestSoup("http://weixin.sogou.com/weixin?type=2&query=" + word + 
                       "&ie=utf8&s_from=input&_sug_=y&_sug_type_=&w=01019900&sut=1713&sst0=1499419256365&lkt=1%2C1499419256260%2C1499419256260")
    # 去掉注释
    for element in soup(text=lambda text: isinstance(text, Comment)):
        element.extract()
    # 结构化处理
    this_search_list = []
    for result in soup.find(class_='news-list').find_all('li', limit=count):
        search = {} #第一遍遍历结果的时候将search初始化
        search['title'] = ''.join([item.string for item in result.find('h3').find('a').contents])
        search['introduce'] = ''.join([item.string for item in result.find(class_='txt-info')])
        search['from_'] = 'gongzhognhao_' + result.find(class_='account').string
        search['url'] = result.find(class_='txt-box').find('a')['href']
        search['image'] = result.find('img')['src'] #搜狗好像会屏蔽不是从搜索跳过来的，之后不行的话就置为''
        search['time'] = time.time()
        this_search_list.append(search)
    return this_search_list


# In[ ]:

def searchDaiZhiGe(word, count):
    # 抓取网页
    soup = requestSoup("http://122.200.75.13/result.php?query==" + word + "&category=")
    # 结构化处理
    this_search_list = []
    for result in soup.find_all('article', limit=count):
        search = {} #第一遍遍历结果的时候将search初始化
        search['title'] = result.find('h3').find('a').string
        search['introduce'] = (''.join([item.string for item in result.find('p').contents]).encode('utf-8').replace('\r\n', ',').replace('　　', '')).decode('utf8')
        search['from_'] = 'daizhige'
        search['url'] = u'http://122.200.75.13' + result.find('h3').find('a')['href']
        search['image'] = ""
        search['time'] = time.time()
        this_search_list.append(search)
    return this_search_list


# In[ ]:

def searchDaoon(word, count):
    # 抓取网页
    soup = requestSoup("https://www.daoon.com/?s=" + word)
    # 结构化处理
    this_search_list = []
    for result in soup.find_all(class_='entry_item', limit=4):
        search = {} #第一遍遍历结果的时候将search初始化 
        try:
            search['title'] = result.find_all('a')[1]['title']
            search['introduce'] = result.find('p').string
            search['from_'] = 'daoon'
            search['url'] =result.find_all('a')[1]['href']
            search['image'] = 'https:' + result.find('img')['src']
            search['time'] = time.time()
        except:
            continue
        this_search_list.append(search)
    return this_search_list


# In[ ]:

def searchShuGe(word, count):
    # 抓取网页
    soup = requestSoup("https://shuge.org/?s=" + word)
    # 结构化处理
    this_search_list = []
    for result in soup.find_all(class_='blogpost', limit=4):
        search = {} #第一遍遍历结果的时候将search初始化
        search['title'] = result.find(class_='blogtitle').find('a').string.strip()
        search['introduce'] = result.find(class_='five_sixth column-last').find_all('p')[1].contents[0]
        search['from_'] = 'shuge'
        search['url'] = result.find(class_='blogtitle').find('a')['href']
        search['image'] = result.find(class_='featuredimage').find('img')['src']
        search['time'] = time.time()
        this_search_list.append(search)
    return this_search_list


# In[ ]:

def getSearchList(word):
    search_list = []
    search_list.extend(searchBaiKe(word,1))
    search_list.extend(searchDouBan(word,2))
#     search_list.extend(searchGongZhongHao(word,3)) 微信公众号采集不了
    search_list.extend(searchDaiZhiGe(word,3))
    search_list.extend(searchDaoon(word,3))
    search_list.extend(searchShuGe(word,3))
    return search_list


# In[ ]:

# construct the argument parser and parse the arguments
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-w", "--word", required = True,
	help = "word")
args = vars(ap.parse_args())
result = getSearchList((args["word"]).decode('gb2312'))
# print 'result:'
print result

