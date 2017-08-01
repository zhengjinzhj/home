# -*- coding:utf-8 -*-

import chardet
import urllib2
import requests
import re
# import xml.etree.ElementTree as etree


def chardet_detect_str_encoding():
    """
        Demo how to use chardet to detect string encoding/charset
    """
    proxy = urllib2.ProxyHandler({'http': '127.0.0.1:8087'})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    response = opener.open('http://www.ftoow.com/thread.php?fid-61-type-82-page-1.html')  # 33, 58, 59, 69,
    inputStr = response.read()  # {'confidence': 0.9614217598612917, 'encoding': 'EUC-JP'}
    # inputStr = 'test'  # we have 100% confidence to say that the input string encoding is ascii
    # inputStr = '当前文件时UTF-8，所以你所看到的这段字符串，也是UTF-8编码的'
    detectedEncodingDict = chardet.detect(inputStr)
    print "type(detectedEncodingDict)=", type(detectedEncodingDict)  # type(detectedEncodingDict)= <type 'dict'>
    print "detectedEncodingDict=", detectedEncodingDict
    # detectedEncodingDict= {'confidence': 0.99, 'encoding': 'utf-8'}
    detectedEncoding = detectedEncodingDict['encoding']
    print "That is, we have %d%% confidence to say that the input string encoding is %s" %\
          (int(detectedEncodingDict['confidence']*100), detectedEncoding)
    # print inputStr.decode('euc-jp').encode('utf-8')

chardet_detect_str_encoding()

# proxy = {'http': '127.0.0.1:8087'}
# r = requests.get('http://www.caribbeancom.com/listpages/all1.htm', proxies=proxy)
# # print r.text
# pattern = re.compile('<a href=\/moviepages\/(.*?)\/index.html.*?'
#                      '<img.*?thumbnail src=(.*?) alt=(.*?) title=(.*?)>.*?movie-date>(.*?)</span>', re.S)
# items = re.findall(pattern, r.text)
# for item in items:
#     print item
