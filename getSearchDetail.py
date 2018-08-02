
# coding: utf-8

# In[3]:


import urllib2
from bs4 import BeautifulSoup, element
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# In[4]:

# 网页解析相关的function
def requestSoup(url):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    content = response.read()
    soup = BeautifulSoup(content, 'lxml')
    return soup
def getStr(item):
    if type(item.string) == element.NavigableString:
        return item.string.strip()
    return ''


# In[5]:

# 采集百度百科
def searchBaike(soup):
    try:
        title = soup.find('title').string
    except:
        title = ''
    try:
        content =  ''.join([getStr(item) for item in soup.find(class_='lemma-summary').descendants])
    except:
        content = ''
    try:
        images = '|||'.join([item['data-src'] for item in soup.find_all(class_='lazy-img',limit=5)])
    except:
        images = ''
    return title, content, images


# In[6]:

# 采集豆瓣读书
def searchDouban(soup):
    try:
        title = ('《').decode('utf8') + soup.find('title').string.replace(('(豆瓣)').decode('utf8'),'').strip() + ('》').decode('utf8')
    except:
        title = ''
    try:
        content = '|||'.join([getStr(item) for item in soup.find(class_='intro').find_all('p')])
    except:
        content = ''
    try:
        images = soup.find(class_='nbg')['href']
    except:
        images = ''
    return title, content, images


# In[7]:

# 采集殆知阁
def searchDaizhige(soup):
    try:
        title = soup.find('title').string
    except:
        title = ''
    try:
        content = '|||'.join([getStr(item) for item in soup.find('span').contents])
    except:
        content = ''
    try:
        images = ''
    except:
        images = ''
    return title, content, images


# In[13]:

# 采集书格
def searchShuge(soup):
    try:
        title = soup.find('title').string
    except:
        title = ''
    try:
        content = ''
        for p in soup.find(class_='four_fifth column-last').find_all('p', recursive=False):
            content += ''.join([getStr(item) for item in p.descendants]) + '|||'
    except:
        content = ''
    try:
        images = '|||'.join([item['src'] for item in soup.find(class_='wmuSliderWrapper').find_all('img')])
    except:
        images = ''
    return title, content, images


# In[9]:

# 采集道印
def searchDaoon(soup):
    try:
        title = soup.find('title').string.replace((' | DAO on | 道卬').decode('utf8'), '')
    except:
        title = ''
    try:
        content = ''
        for p in soup.find_all('p'):
            content += ''.join([getStr(item) for item in p.descendants]) + '|||'
    except:
        content = ''
    try:
        images = '|||'.join([('https:' + item['src']) for item in soup.find_all(class_='attachment-post_image size-post_image')])
    except:
        images = ''
    return title, content, images


# In[10]:

# 采集详情
def searchDetail(url, from_):
    # 采集
    soup = requestSoup(url)
    if from_ == 'baidubaike':
        title, content, images = searchBaike(soup)
    elif from_ == 'doubandushu':
        title, content, images = searchDouban(soup)
    elif from_ == 'daizhige':
        title, content, images = searchDaizhige(soup)
    elif from_ == 'shuge':
        title, content, images = searchShuge(soup)
    elif from_ == 'daoon':
        title, content, images = searchDaoon(soup)
    # 返回给前端
    return url, title, content ,images, from_


# In[ ]:

# construct the argument parser and parse the arguments
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--url", required = True,
	help = "url")
ap.add_argument("-f", "--from", required = True,
	help = "from")
args = vars(ap.parse_args())
result = searchDetail(args["url"], args['from'])
print 'result:'
print result

