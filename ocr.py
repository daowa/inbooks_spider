
# coding: utf-8

# In[1]:


import urllib, urllib2, sys
import ssl
import time
import base64
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# In[2]:

def read_access_token():
    f = open('E:\\work\\inBook\\data\\access_token.txt')
    line = f.readline()
    access_token = line.split(',')[0]
    timestamp = float(line.split(',')[1])
    if (time.time()-timestamp) > 1641600: #更新日期在20天以上，则重新获取access_token
        # 获取access_token
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=g1DGXp8jQ85fIbUNOsamQGQ0&client_secret=Lv0N33c20jBPxn3hvslsPPX45TjxgXSU'
        request = urllib2.Request(host)
        request.add_header('Content-Type', 'application/json; charset=UTF-8')
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        response = urllib2.urlopen(request, context=ctx)
        content = response.read()
        if content:
            access_token = eval(content)['access_token']
        # 写入file
        f = open('E:\\work\\inBook\\data\\access_token.txt', 'w')
        f.write(access_token + ',' + str(time.time()))
    return access_token


# In[3]:

def get_content(image_path):
    access_token = read_access_token()
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=' + access_token
    f=open(image_path,'rb') #二进制方式打开图文件
    img=base64.b64encode(f.read())
    params= {"image": img}
    params = urllib.urlencode(params)
    request = urllib2.Request(url, params)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib2.urlopen(request)
    content = response.read()
    if content:
        result = [item['words'] for item in eval(content)['words_result']]
        content = ''.join(result)
    return content


# In[12]:

# construct the argument parser and parse the arguments
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "image_url")
args = vars(ap.parse_args())
content = get_content(args['image'])
print 'result:' + content.decode('utf8')


# In[ ]:



