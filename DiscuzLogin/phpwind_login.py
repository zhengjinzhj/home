# -*- coding:utf-8 -*-

# from urllib import urlencode
# import cookielib
# import urllib2
#
# # cookie
# cj = cookielib.LWPCookieJar()
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
# urllib2.install_opener(opener)
#
# # Login
# user_data = {'pwuser': 'naobing', 'pwpwd': 'naobing123', 'step': '2'}
# url_data = urlencode(user_data)
# login_r = opener.open("http://www.ftoow.com/login.php", url_data)
#
# request = urllib2.Request('http://www.ftoow.com/u.php')
# response = urllib2.urlopen(request).read()
# response = response.decode('gbk').encode('utf-8')
# print response

import requests
import re

_url = 'http://www.ftoow.com/login.php'
_data = {'lgt': 0, 'pwuser': 'naobing', 'pwpwd': 'naobing123', 'jumpurl': 'http://www.ftoow.com/index.php',
         'ajax': 1, 'step': 2, 'cktime': 31536000, 'verify': ''}
r = requests.post(_url, data=_data)
_cookies = r.cookies

# 获取到_cookies后再访问u.php页面获取一个verify字符串（这时候就需要代入cookies参数了）
r = requests.get('http://www.ftoow.com/u.php', cookies=_cookies)
_content = r.content
print _content.decode('gbk').encode('utf-8')
verify = re.compile(r'var verifyhash = \'(.*?)\';', re.I).findall(_content)
print verify

# 然后继续代入_cookies并访问打卡url（需要第二部抓取到的verify）
requests.get('http://www.ftoow.com/jobcenter.php?action=punch&step=2&verify=%s' % verify, cookies=_cookies)

# http://www.ftoow.com/jobcenter.php?action=punch&verify=90d7384b76a5d263&nowtime=1474904612188&verify=90d7384b76a5d263
