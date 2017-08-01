# -*- coding:utf-8 -*-

import cookielib
import re
import urllib
import urllib2

import config


class Discuz(object):
    def __init__(self):
        self.operate = ''  # response的对象（不含read）
        self.formhash = ''  # 没有formhash不能发帖

        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)

        self.formhash_pattern = re.compile(r'<input type="hidden" name="formhash" value="([0-9a-zA-Z]+)" />')

    def login(self, username, password, questionid=0, answer=''):
        postdata = {
                    'loginfield': config.LOGINFIELD,
                    'username': username,
                    'password': password,
                    'questionid': questionid,
                    'answer': answer,
                    'cookietime': config.COOKIETIME,
                    }

        login_success_pattern = re.compile(ur"\('succeedlocation'\).innerHTML = '(?u)(.+)，现在将转入登录前页面';")
        login_fail_pattern = re.compile(r"{errorhandle_\('(?u)(.+)', {'loginperm':")

        # 取得登录成功/失败的提示信息
        self.operate = self._get_response(config.LOGINURL, postdata)
        login_tip_page = self.operate.read().decode('utf-8')
        login_success_info = login_success_pattern.search(login_tip_page)
        login_fail_info = login_fail_pattern.search(login_tip_page)

        # 显示登录成功/失败信息
        if login_success_info:
            print login_success_info.group(1)
            self.formhash = self._get_formhash(self._get_response(config.DOMAIN).read())
            return True
        elif login_fail_info:
            print login_fail_info.group(1)
        else:
            print '无法获取登录状态'

        return False

    def _get_response(self, url, data=None):
        if data is not None:
            req = urllib2.Request(url, urllib.urlencode(data))
        else:
            req = urllib2.Request(url)

        response = self.opener.open(req)
        return response

    def _get_formhash(self, page_content):
        self.formhash = self.formhash_pattern.search(page_content.decode('gbk')).group(1)
        return self.formhash
