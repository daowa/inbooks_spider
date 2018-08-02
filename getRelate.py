
# coding: utf-8

# In[ ]:


import urllib2
from bs4 import BeautifulSoup, element, Comment
import MySQLdb
import re
import sys
reload( sys )
sys.setdefaultencoding('utf-8')


# In[ ]:

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
def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))


# In[ ]:

# 判断是否已经从百度百科获得关系
def isBaiked(word):
    cur = conn.cursor()
    count = cur.execute('select * from inbook.entity where word="' + word + '"')
    if count == 0: #无该记录，则插入，并返回False
        cur.execute('insert into inbook.entity values("' + word + '",0)')
        conn.commit()
        return False
    else: #有该记录，判断是否录入百科了
        data = cur.fetchone()
        if data[1] == 0: #未录入，则返回False
            return False
    return True
    cur.close()


# In[ ]:

# 获取关系
def getBaikeRelate(word1):
#     try:
    soup = requestSoup("http://baike.baidu.com/item/" + word1)
#     except:
#         print 'getBaikeRelate - soup eroor'
#         return []
    word1 = word1.decode("utf8")
    list_word2_relate = []
    # 读取属性
    result = soup.find(class_='basic-info')
    if result is None:
        pass
    else:
        try:
            for a in result.find_all('a'):
                word2 = getStr(a)
                if hasNumbers(word2): continue #目前不把包含阿拉伯数字的认为是实体
                relate = a.parent.previous_sibling.previous_sibling.string.replace(' ', '')
                relate = ''.join(relate.split()).replace("\n","") #去中间空格
                if len(word2)>1  and len(word2)<15 and len(relate) < 10:
                    list_word2_relate.append([word1, word2, relate, 'baike'])
            # 读取页面所有实体
            word2s = []
            for result in soup.find_all('a', target='_blank', href=re.compile('/item/%.*')):
                word2 = getStr(result) + ''
                if word2 in word2s: #避免一个词多次录入
                    continue
                else:
                    word2s.append(word2)
                if hasNumbers(word2): continue #目前不把包含阿拉伯数字的认为是实体
                if ('义项').decode('utf8') in word2: continue
                relate = ''.join([getStr(item) for item in result.parent.contents]).replace("\n","")
                if len(word2)>1 and len(word2)<15 and len(word1)<25 and len(relate) < 400:
                    list_word2_relate.append([word1, word2, relate, 'baike'])
        except:
            print 'getBaikeRelate - error'
    # 读取相关关系
    return list_word2_relate


# In[ ]:

#将关系写入数据库
def setBaikeRelate(list_relate):
    curs = conn.cursor()
    try:
        curs.executemany("insert into inbook.relate(word1, word2, relate, from_) values(%s,%s,%s,%s)", list_relate)
    except:
        print 'setBaikeRelate error'
    conn.commit()
    curs.close()


# In[ ]:

#将实体写入数据库
def setEntity(list_relate):
    cur = conn.cursor()
    # 获取数据库中已有的id
    cur.execute('select word from inbook.entity')
    results = cur.fetchall()
    words = [result[0] for result in results]
    # 对比去重
    new_words = [l[1] for l in list_relate]
    new_words = list(set(new_words).difference(set(words)))
    # 将新增的实体写入数据库
    try:
        cur.executemany('insert into inbook.entity(word) values(%s)', new_words)
        conn.commit()
    except:
        print 'setEntity - insert error'
    cur.close()


# In[ ]:

#将entity中的baiked改为1
def setBaiked(word):
    try:
        cur = conn.cursor()
        cur.execute('update inbook.entity set baiked = 1 where word="' + word + '"')
        conn.commit()
        cur.close()
    except:
        print 'setBaiked - update error'


# In[ ]:

def getRelate(word):
    global conn
    conn=MySQLdb.connect(host='localhost',user='inbook',passwd='abcd@123',db='inbook',port=3306,charset='utf8')
    if isBaiked(word) == False: #仅当该词关系未被采集时，采集关系
        list_relate = getBaikeRelate(word) #获取关系
        setBaikeRelate(list_relate) #将关系写入数据库
        setEntity(list_relate) #将实体写入数据库
        setBaiked(word) #将entity中的baiked改为1
    conn.close()


# In[ ]:

# construct the argument parser and parse the arguments
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-w", "--word", required = True,
	help = "word")
args = vars(ap.parse_args())
getRelate((args["word"]).decode('gb2312'))
print 'result:ok'


# In[ ]:

# # 全循环
# conn=MySQLdb.connect(host='localhost',user='root',passwd='abcd@123',db='inbook',port=3306,charset='utf8')
# cur = conn.cursor()
# cur.execute('select word from inbook.entity where baiked = 0')
# results = cur.fetchall()
# for r in results:
#     print (r[0]).encode('utf8')
#     getRelate((r[0]).encode('utf8'))
# conn.close()


# In[ ]:



