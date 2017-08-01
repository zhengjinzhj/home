# -*- coding: utf-8 -*-

import urllib2
import urllib
import cookielib
import re

'''
  通用的登陆DZ论坛
  参数说明parms:
      username: 用户名(必填),
      password: 密码(必填),
      domain: 网站域名，格式必须是：http://www.xxx.xx/(必填),
      questionid: 安全提问，默认是0,
      answer: 安全提问的答案，默认是空字符串,
      referer: 登录后跳转到的目的网页，不过由于登录后会出现登录成功/失败的提示信息，5s后才会转到目的网页

  这里使用了可变关键字参数(相关信息可参考手册)
'''


def login_dz(**parms):

    # 初始化
    parms_key = ['domain', 'username', 'password', 'questionid', 'answer', 'referer']
    arg = {}
    for key in parms_key:
        if key in parms:
            arg[key] = parms[key]
        else:
            arg[key] = ''
    # print parms
    # print parms['username']
    print arg

    # cookie设置
    cookie_file = 'cookies.dat'
    cookie = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

    # 获取formhash，formhash是一个验证数据，在登录前后不同，登录前的formhash可以忽略
    # 但登录后的formhash需要读取出来，否则发帖时会提示“您的来路请求不正确”的错误。
    pre_login = arg['domain']+'member.php?mod=logging&action=login&' \
                              'infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login'
    c = opener.open(pre_login).read()
    cookie.save(cookie_file)
    # print c
    patt = re.compile(r'.*?name="formhash".*?value="(.*?)".*?')
    formhash = patt.search(c)
    print formhash
    if not formhash:
        raise Exception('GET formhash Fail!')
    formhash = formhash.group(1)
    print formhash

    # 登录
    postdata = {
     'answer': arg['answer'],
     'formhash': formhash,
     'password': arg['password'],
     'questionid': 0 if arg['questionid'] == '' else arg['questionid'],
     'referer': arg['domain'] if arg['referer'] == '' else arg['referer'],
     'username': arg['username'],
    }

    postdata = urllib.urlencode(postdata)
    req = urllib2.Request(
        url=arg['domain'] +
        'member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash=LCaB3&inajax=1',
        data=postdata
        )
    c = opener.open(req).read(300)
    flag = '登录失败 %s' % arg['username']
    if 'succeedhandle_login' in c:
        flag = True
    return flag


# 使用例子：基本参数登录
if __name__ == '__main__':
    username = r'naobing'  # 如果用户名为汉字，需要在r前面加u。
    password = 'naobing123'
    domain = 'http://www.ftoow.com/'  # 另一个测试网站：http://www.kafan.cn/
    try:
        result = login_dz(username=username, password=password, domain=domain)
        print(result)
    except Exception, e:
        print('Error:', e)
