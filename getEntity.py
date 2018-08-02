
# coding: utf-8

# In[ ]:


import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import jieba
import jieba.posseg as pseg
import urllib
import json
import os
import re
import socket
socket.setdefaulttimeout(10)


# In[ ]:

# # 将数据库中的实体词导入到txt中，平时不使用
# import MySQLdb
# conn=MySQLdb.connect(host='localhost',user='root',passwd='abcd@123',db='inbook',port=3306,charset='utf8')
# cur = conn.cursor()
# cur.execute('select word from inbook.entity')
# result = cur.fetchall()
# f = open('E:\\work\\inBook\\data\\entity.txt','w')
# for i in result:
#     if len(i) > 0:
#         f.write(str(i[0].encode('utf8')) + ' 200 nz\r\n')
# f.close()
# cur.close()
# conn.close()


# In[ ]:

# 加载用户词典
jieba.load_userdict('..\\data\\entity.txt')


# In[ ]:

# 从LTP获取命名实体词
def getLTP(txt):
    url_get_base = "http://api.ltp-cloud.com/analysis/"
    args = { 
        'api_key' : '3192q2F231PbkmmpFt9fAUTZLDjhHYiWhMLXNi6f',
        'text' : txt,
        'pattern' : 'ner',
        'format' : 'plain',
        'only_ner' : 'true'
    }
    content = ''
    try:
        result = urllib.urlopen(url_get_base, urllib.urlencode(args)) # POST method
        content = result.read()
        result.close()
    except:
        pass
    return [item.split(' ')[0].decode('utf-8') for item in content.split('\n')]


# In[ ]:

# 从jieba获取命名实体词
def getJIEBA(txt):
    result = []
    for w in pseg.cut(txt):
        if (w.flag == 'ns') or (w.flag == 'nh') or (w.flag == 'ni') or (w.flag == 'nz'):
            if len(w.word) < 2: continue #实体最短长度为2
            result.append(w.word)
    return result


# In[ ]:

# 获取命名实体词
def getEntity(txt):
#     return list(set(ltp(txt) + jieba(txt)))
    return sorted(list(set(getJIEBA(txt))), key=lambda x: len(x), reverse=True)


# In[ ]:

# construct the argument parser and parse the arguments
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--content", required = True,
	help = "content")
args = vars(ap.parse_args())
result = getEntity((args["content"]).decode('gb2312'))
print 'result:'
print result

