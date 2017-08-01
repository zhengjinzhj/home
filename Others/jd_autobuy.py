#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from hashlib import md5
import random
import json
import time
import re
from bs4 import BeautifulSoup


class RkClient:

    def __init__(self, username, password):
        self.username = username
        self.password = md5(password.encode('utf-8')).hexdigest()
        self.soft_id = 80032
        self.soft_key = '8c37f5b5c5784e2ebe7681f4ff325cee'
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben'
        }

    def rk_create(self, im, im_type, timeout=60):

        # im: 图片字节
        # im_type: 题目类型

        params = {
            'typeid': im_type,
            'timeout': timeout
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        rk = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
        return rk.json()

    def rk_report_error(self, im_id):

        # im_id:报错题目的id（rk_create方法会返回）

        params = {'id': im_id}
        params.update(self.base_params)
        rr = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return rr.json()


# rc = RkClient('naobing', 'naobing123')
# im = open('a.jpg', 'rb').read()
# print(rc.rk_create(im, 3040))

# ====================================================


class JD(object):

    def __init__(self, username, password, rk_username, rk_password):
        self.username = username
        self.password = password
        self.rk_client = RkClient(rk_username, rk_password)
        self.track_id = ''
        self.pid = ''

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive'
        }

        self.session = requests.session()

        self.cookie = {}

    @staticmethod
    def response_status(resp):
        if resp.status_code != requests.codes.OK:
            print('Status: %u, Url: %s' % (resp.status_code, resp.url))
            return False
        return True

    def _need_auth_code(self):

        # check if need auth code
        self.headers['X-Requested-With'] = 'XMLHttpRequest'
        auth_url = 'https://passport.jd.com/uc/showAuthCode'
        auth_dat = {
            'loginName': self.username,
        }
        payload = {
            'r': random.random(),
            'version': 2015
        }

        resp = self.session.post(auth_url, data=auth_dat, params=payload, headers=self.headers)
        if self.response_status(resp):
            js = json.loads(resp.text[1:-1])
            return js['verifycode']

        print('获取是否需要验证码失败')
        return False

    def login(self):

        login_url = 'https://passport.jd.com/new/login.aspx'
        login_request_url = 'https://passport.jd.com/uc/loginService'
        resp = self.session.get(login_url, headers=self.headers)
        soup = BeautifulSoup(resp.text, 'html.parser')

        for k, v in resp.cookies.items():
            self.cookie[k] = v

        params = {
            'uuid': soup.find(id='uuid')['value'],
            'eid': soup.find(id='eid')['value'],
            '_t': soup.find(id='token')['value'],
            'fp': soup.find(id='sessionId')['value'],
            'loginType': 'c',
            'loginname': self.username,
            'nloginpwd': self.password,
            'chkRememberMe': '',
            'authcode': '',
            'pubKey': soup.find(id='pubKey')['value'],
            'sa_token': soup.find(id='sa_token')['value']
        }

        self.headers['Referer'] = 'https://passport.jd.com/new/login.aspx'

        if self._need_auth_code():  # 若需要验证码
            img_code_url = soup.find(id='JD_Verification1')['src2']
            img = requests.get('http:' + img_code_url)
            with open('C:\\Users\\Administrator\\PycharmProjects\\work\\a.jpg', 'wb') as f:
                f.write(img.content)
            im = open('a.jpg', 'rb').read()
            print('开始识别验证码...')

            # 自动打码（识别验证码）
            img_code = self.rk_client.rk_create(im, 3040)['Result']
            print(img_code)
            params['authcode'] = img_code

        resp = self.session.post(
            login_request_url,
            data=params,
            cookies=self.cookie,
            headers=self.headers)

        # login_request.text is something like ({"success":"//www.jd.com"})
        result = json.loads(resp.text[1:-1])
        print(result)
        if result.get('success'):
            print('登录成功！')
            self.track_id = self.session.cookies['TrackID']
            for k, v in resp.cookies.items():
                self.cookie[k] = v
        else:
            print('登录失败，再次登录中...')
            # time.sleep(10)
            # self.login()

    def add_cart(self):
        self.pid = input('请输入要加入购物车的商品编号：')
        pcount = input('请输入加入数量：')

        # add_carturl = 'https://cart.jd.com/gate.action?pid=3659204&pcount=1&ptype=1'
        add_cart_url = 'https://cart.jd.com/gate.action?pid='+self.pid+'&pcount='+pcount+'&ptype=1'
        add_cart_request = session.get(add_cart_url)

        if re.compile('<title>(.*?)</title>').findall(add_cart_request.text)[0] == '商品已成功加入购物车':
            print('商品已成功加入购物车!')
        else:
            print('商品加入购物车失败！！！请再试一次')
            self.add_cart()

    def submit(self):
        cart_url = 'https://cart.jd.com'
        req5 = session.get(cart_url)
        form_data = {
            'outSkus': '',
            'pid': self.pid,
            'ptype': '1',
            'packId': '0',
            'targetId': '0',
            'promoID': '0',
            'locationId': '22-1930-50945-52160'  # 地址代码
        }

        select_item_url = 'https://cart.jd.com/selectItem.action?rd' + str(random.random())
        req7 = session.post(select_item_url, data=form_data)
        order_submit_url = 'https://trade.jd.com/shopping/order/submitOrder.action'

        submit_data = {
            'overseaPurchaseCookies': '',
            'submitOrderParam.sopNotPutInvoice': 'false',
            'submitOrderParam.trackID': self.track_id[0],
            'submitOrderParam.ignorePriceChange': '0',
            'submitOrderParam.btSupport': '0',
            'submitOrderParam.eid': eid,
            'submitOrderParam.fp': 'b31fc738113fbc4ea5fed9fc9811acc6'
        }

        order_time = input('请选择下单时间：1.设置下单时间；2.立即下单（可用于监控库存，自动下单）：')

        if order_time == '1':
            set_time = input('请按照2017-05-01 23:11:11格式输入下单时间:')
            time_array = time.mktime(time.strptime(set_time, '%Y-%m-%d %H:%M:%S'))
            while True:
                if time.time() >= time_array:
                    print('正在提交订单...')
                    req8 = session.post(order_submit_url, data=submit_data)
                    js1 = json.loads(req8.text)
                    # print(js1)
                    if js1['success'] is True:
                        print('下单成功！')
                    else:
                        print('下单失败！')
                    break
                else:
                    # print('等待下单...')
                    continue
        elif order_time == '2':
            while True:
                area = '22-1930-50945-52160'  # 地址编码
                stock_url = 'http://c0.3.cn/stocks?callback=jQuery2289454&type=getstocks&skuIds=' + self.pid\
                            + '&area=' + area + '&_=1490694504044'
                resp = session.get(stock_url)
                jsparser = json.loads(resp.text)
                print(jsparser)
                # 33-有货, 34-无货
                if jsparser['stock']['StockState'] == 33 and jsparser['stock']['StockStateName'] == '现货':
                    print('库存状态：', jsparser['stock']['StockStateName'])

                    req8 = session.post(order_submit_url, data=submit_data)
                    print('正在提交订单...')
                    js1 = json.loads(req8.text)
                    if js1['success'] is True:
                        print('下单成功！')
                        break
                    else:
                        print('下单失败！')
                        # 3秒后重新尝试下单，可自行修改时间间隔
                        time.sleep(3)
                        continue
                else:
                    print('无货，监控中...')
                    time.sleep(3)
                    continue

# jd_user = input('请输入京东账号:')
# jd_pwd = input('请输入京东密码:')
# rk_user = input('请输入若快账号:')
# rk_pwd = input('请输入若快密码:')
demo = JD('zheng_jin', 'zhengjin341281', 'naobing', 'naobing123')
print('正在登录...')
# print(demo._need_auth_code())
demo.login()
# demo.add_cart()
# demo.submit()











