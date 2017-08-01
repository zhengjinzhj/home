#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import random
import time
import json
from bs4 import BeautifulSoup


class JDWrapper(object):
    """
    This class used to simulate login JD
    """

    def __init__(self, usr_name=None, usr_pwd=None):
        # cookie info
        self.trackid = ''
        self.uuid = ''
        self.eid = ''
        self.fp = ''

        self.usr_name = usr_name
        self.usr_pwd = usr_pwd

        self.interval = 0

        # init url related
        self.home = 'https://passport.jd.com/new/login.aspx'
        self.login = 'https://passport.jd.com/uc/loginService'
        self.imag = 'https://authcode.jd.com/verify/image'
        self.auth = 'https://passport.jd.com/uc/showAuthCode'

        self.sess = requests.Session()

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/'
                          '537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'ContentType': 'text/html; charset=utf-8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
        }

        self.cookies = {}

    def log_in(self):
        resp = self.sess.get(
            self.home,
            headers=self.headers
        )
        for k, v in resp.cookies.items():
            self.cookies[k] = v

        soup = BeautifulSoup(resp.text, 'html.parser')
        self.uuid = soup.select('#uuid')[0]['value']
        self.eid = soup.select('#eid')[0]['value']
        self.fp = soup.select('#sessionId')[0]['value']
        data = {
            'uuid': self.uuid,
            'eid': self.eid,
            'fp': self.fp,
            '_t': soup.select('#token')[0]['value'],
            'loginType': soup.select('#loginType')[0]['value'],
            'loginname': self.usr_name,
            'nloginpwd': self.usr_pwd,
            'chkRememberMe': '',
            'authcode': '',
            'pubkey': soup.select('#pubKey')[0]['value'],
            'sa_token': soup.select('#sa_token')[0]['value'],
            'seqSid': ''
        }
        payload = {
            'uuid': self.uuid,
            'r': random.random(),
            'version': 2015
        }

        resp = self.sess.post(
            self.login,
            headers=self.headers,
            data=data,
            params=payload
        )
        print(resp.status_code)
        print(json.loads(resp.text[1:-1]))


demo = JDWrapper(usr_name='zheng_jin', usr_pwd='zhengjin341281')
demo.log_in()


































