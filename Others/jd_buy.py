#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JD online shopping helper tool
-----------------------------------------------------

only support to login by QR code, 
username / password is not working now.

"""

import os
import time
import json
import random
import pickle
import bs4
import requests
import argparse
# import pprint

# get function name
# FuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name


def tags_val(tag, key='', index=0):
    """
    return html tag list attribute @key @index
    if @key is empty, return tag content, mainly ie. for soup.select
    """
    if len(tag) == 0 or len(tag) <= index:
        return ''
    elif key:
        txt = tag[index].get(key)
        return txt.strip(' \t\r\n') if txt else ''
    else:
        txt = tag[index].text
        return txt.strip(' \t\r\n') if txt else ''


def tag_val(tag, key=''):
    """
    return html tag attribute @key
    if @key is empty, return tag content, mainly ie. for soup.find
    """
    if tag is None: 
        return ''
    elif key:
        txt = tag.get(key)
        return txt.strip(' \t\r\n') if txt else ''
    else:
        txt = tag.text
        return txt.strip(' \t\r\n') if txt else ''


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

    # @staticmethod
    # def print_json(resp_text):
    #     """
    #     format the response content
    #     """
    #     if resp_text[0] == '(':
    #         resp_text = resp_text[1:-1]
    #
    #     for k, v in json.loads(resp_text).items():
    #         print('%s: %s' % (k, v))

    @staticmethod
    def response_status(resp):
        if resp.status_code != requests.codes.OK:
            print('Status: %u, Url: %s' % (resp.status_code, resp.url))
            return False
        return True

    # def _need_auth_code(self, usr_name):
    #     # check if need auth code
    #     #
    #     auth_dat = {
    #         'loginName': usr_name,
    #     }
    #     payload = {
    #         'r': random.random(),
    #         'version': 2015
    #     }
    #
    #     resp = self.sess.post(self.auth, data=auth_dat, params=payload)
    #     if self.response_status(resp):
    #         js = json.loads(resp.text[1:-1])
    #         return js['verifycode']
    #
    #     print('获取是否需要验证码失败')
    #     return False

    # def _get_auth_code(self, uuid):
    #     # image save path
    #     image_file = os.path.join(os.getcwd(), 'authcode.jfif')
    #
    #     payload = {
    #         'a': 1,
    #         'acid': uuid,
    #         'uid': uuid,
    #         'yys': str(int(time.time() * 1000)),
    #     }
    #
    #     # get auth code
    #     r = self.sess.get(self.imag, params=payload)
    #     if not self.response_status(r):
    #         print('获取验证码失败')
    #         return False
    #
    #     with open(image_file, 'wb') as f:
    #         for chunk in r.iter_content(chunk_size=1024):
    #             f.write(chunk)
    #
    #         f.close()
    #
    #     os.system('start ' + image_file)
    #     return str(input('Auth Code: '))

    # def _login_once(self, login_data):
    #     # url parameter
    #     payload = {
    #         'r': random.random(),
    #         'uuid': login_data['uuid'],
    #         'version': 2015,
    #     }
    #
    #     resp = self.sess.post(self.login, data=login_data, params=payload)
    #     if self.response_status(resp):
    #         js = json.loads(resp.text[1:-1])
    #         # self.print_json(resp.text)
    #
    #         if not js.get('success'):
    #             print(js.get('emptyAuthcode'))
    #             return False
    #         else:
    #             return True
    #
    #     return False

    # def _login_try(self):
    #     """ login by username and password, but not working now.
    #     
    #     .. deprecated::
    #         Use `login_by_QR`
    #     """
    #     # get login page
    #     #resp = self.sess.get(self.home)
    #     print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    #     print('{0} > 登录'.format(time.ctime()))
    # 
    #     try:
    #         # 2016/09/17 PhantomJS can't login anymore
    #         self.browser.get(self.home)
    #         soup = bs4.BeautifulSoup(self.browser.page_source, "html.parser")
    #         
    #         # set cookies from PhantomJS
    #         for cookie in self.browser.get_cookies():
    #             self.sess.cookies[cookie['name']] = str(cookie['value'])
    # 
    #         #for (k, v) in self.sess.cookies.items():
    #         #	print('%s: %s' % (k, v)
    #             
    #         # response data hidden input == 9 ??. Changed 
    #         inputs = soup.select('form#formlogin input[type=hidden]')
    #         rand_name = inputs[-1]['name']
    #         rand_data = inputs[-1]['value']
    #         token = ''
    # 
    #         for idx in range(len(inputs) - 1):
    #             id = inputs[idx]['id']
    #             va = inputs[idx]['value']
    #             if   id == 'token':
    #                 token = va
    #             elif id == 'uuid':
    #                 self.uuid = va
    #             elif id == 'eid':
    #                 self.eid = va
    #             elif id == 'sessionId':
    #                 self.fp = va
    #         
    #         auth_code = ''
    #         if self.need_auth_code(self.usr_name):
    #             auth_code = self.get_auth_code(self.uuid)	
    #         else:
    #             print('无验证码登录')
    #         
    #         login_data = {
    #             '_t': token,
    #             'authcode': auth_code,
    #             'chkRememberMe': 'on',
    #             'loginType': 'f',
    #             'uuid': self.uuid,
    #             'eid': self.eid,
    #             'fp': self.fp,
    #             'nloginpwd': self.usr_pwd,
    #             'loginname': self.usr_name,
    #             'loginpwd': self.usr_pwd,
    #             rand_name: rand_data,
    #         }
    #         
    #         login_succeed = self.login_once(login_data)
    #         if login_succeed:
    #             self.trackid = self.sess.cookies['TrackID']
    #             print('登录成功 %s' % self.usr_name)
    #         else:		
    #             print('登录失败 %s' % self.usr_name)	
    # 
    #         return login_succeed
    # 
    #     except Exception:
    #         print('Exception:', Exception)
    #         raise
    #     finally:
    #         self.browser.quit()

        # return False    
    
    def login_by_qr(self):
        # jd login by QR code
        try:
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print('{0} > 请打开京东手机客户端，准备扫码登录:'.format(time.ctime()))

            urls = (
                'https://passport.jd.com/new/login.aspx',
                'https://qr.m.jd.com/show',
                'https://qr.m.jd.com/check',
                'https://passport.jd.com/uc/qrCodeTicketValidation'
            )

            # step 1: open login page, fetch cookie for step 2.
            # GET /new/login.aspx HTTP/1.1
            resp = self.sess.get(
                urls[0], 
                headers=self.headers
            )
            if resp.status_code != requests.codes.OK:
                print('获取登录页失败: %u' % resp.status_code)
                return False

            # save cookies
            for k, v in resp.cookies.items():
                self.cookies[k] = v

            # step 2: get QR image, use the cookie got from step 1 to fetch wlfstk_smdl for step 3.
            # GET /show?appid=133&size=147&t=1499672093046 HTTP/1.1
            resp = self.sess.get(
                urls[1], 
                headers=self.headers,
                cookies=self.cookies,
                params={
                    'appid': 133,
                    'size': 147,
                    't': int(time.time() * 1000)
                }
            )
            # 默认情况下，当进行网络请求后，响应体会立即被下载。可以通过stream参数(stream=True)覆盖这个行为，
            # 推迟下载响应体直到访问response.content属性。可以通过调用iter_content并通过设置分块大小参数进行分块的迭代。
            if resp.status_code != requests.codes.OK:
                print('获取二维码失败: %u' % resp.status_code)
                return False
            # save cookies
            for k, v in resp.cookies.items():
                self.cookies[k] = v

            # save QR code
            image_file = 'qr.png'
            with open(image_file, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=1024):
                    f.write(chunk)
            
            # scan QR code with phone
            os.system('start ' + image_file)

            # step 3： check scan result, mush have
            # use wlfstk_smdl got from step 2 to check the QR code status
            # get the ticket when the QR code is scanned and validated(logged in)
            # GET /check?callback=jQuery324169&appid=133&token=16kam16v8sex0orj2y7kz&_=1499680117428 HTTP/1.1
            self.headers['Host'] = 'qr.m.jd.com' 
            self.headers['Referer'] = 'https://passport.jd.com/new/login.aspx'

            # check if QR code scanned
            qr_ticket = None
            retry_times = 100
            while retry_times:
                retry_times -= 1
                resp = self.sess.get(
                    urls[2],
                    headers=self.headers,
                    cookies=self.cookies,
                    params={
                        'callback': 'jQuery%d' % random.randint(100000, 999999),
                        'appid': 133,
                        'token': self.cookies['wlfstk_smdl'],
                        '_': int(time.time() * 1000)
                    }
                )

                # if resp.status_code != requests.codes.OK:
                #     continue

                # jQuery946075({"code" : 201,"msg" : "二维码未扫描 ，请扫描二维码"})
                n1 = resp.text.find('(')
                n2 = resp.text.find(')')
                rs = json.loads(resp.text[n1+1:n2])

                if rs['code'] == 200:
                    # print('{}: {}'.format(rs['code'], rs['ticket']))
                    qr_ticket = rs['ticket']
                    break
                else:
                    print('{}: {}'.format(rs['code'], rs['msg']))
                    time.sleep(10)
            
            if not qr_ticket:
                print('二维码登录失败')
                return False
            
            # step 4: validate scan result, must have, mainly fetch the COOKIE after logged in
            # 其实只要第3步返回200和ticket就已经登录成功，这里只是用第3步拿到的ticket去拿登录后cookie
            # GET /uc/qrCodeTicketValidation?t=AAEAINYCfFakBEpYXnswXIWlGx8utqWe53KBdD3zXryYhj1h HTTP/1.1
            self.headers['Host'] = 'passport.jd.com'
            # self.headers['Referer'] = 'https://passport.jd.com/uc/login?ltype=logout'
            self.headers['Referer'] = 'https://passport.jd.com/new/login.aspx'
            resp = self.sess.get(
                urls[3], 
                headers=self.headers,
                cookies=self.cookies,
                params={'t': qr_ticket},
            )

            if resp.status_code != requests.codes.OK:
                print('二维码登录校验失败: %u' % resp.status_code)
                return False
            
            # login succeed
            self.headers['P3P'] = resp.headers.get('P3P')
            for k, v in resp.cookies.items():
                self.cookies[k] = v
            
            print('登录成功')
            # return True
            return self.cookies
        
        except Exception as e:
            print('Exp:', e)
            raise

    @staticmethod
    def save_cookies(requests_cookies, filename):
        with open(filename, 'wb') as f:
            pickle.dump(requests_cookies, f)

    @staticmethod
    def load_cookies(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)

    def check_cookies(self):

        if not os.path.isfile('jd_cookies'):
            print('Cookie file does not exits!')
            self.cookies = self.login_by_qr()
            self.save_cookies(self.cookies, 'jd_cookies')

        else:
            self.cookies = self.load_cookies('jd_cookies')

        test_url = 'http://home.jd.com/'  # My page
        rs = self.sess.get(test_url, headers=self.headers, cookies=self.cookies, allow_redirects=False)
        if rs.status_code == 200:
            print('jd.com is logged in and jd_cookies is usable!')
            return True
        else:
            self.save_cookies(self.login_by_qr(), 'jd_cookies')
            self.check_cookies()
    
    def good_stock(self, stock_id, area_id=None):
        """
        33: on sale, 
        34: out of stock
        """
        # http://ss.jd.com/ss/areaStockState/mget?app=cart_pc&ch=1&skuNum=3180350,1&area=1,72,2799,0
        # response: {"3180350":{"a":"34","b":"1","c":"-1"}}
        # stock_url = 'http://ss.jd.com/ss/areaStockState/mget' 

        # http://c0.3.cn/stocks?callback=jQuery2289454&type=getstocks&skuIds=3133811&area=1_72_2799_0&_=1490694504044
        # jQuery2289454({"3133811":{"StockState":33,"freshEdi":null,"skuState":1,"PopType":0,"sidDely":"40",
        # "channel":1,"StockStateName":"现货","rid":null,"rfg":0,"ArrivalDate":"","IsPurchase":true,"rn":-1}})
        # jsonp or json both work
        stock_url = 'http://c0.3.cn/stocks' 

        payload = {
            'type': 'getstocks',
            'skuIds': str(stock_id),
            'area': area_id or '22_1930_50945_52160',  # area change as needed
        }
        
        try:
            # get stock state
            resp = self.sess.get(stock_url, params=payload)
            if not self.response_status(resp):
                print('获取商品库存失败')
                return 0, ''
            
            # return json
            resp.encoding = 'gbk'
            stock_info = json.loads(resp.text)
            # print(stock_info)
            stock_stat = int(stock_info[stock_id]['StockState'])
            stock_stat_name = stock_info[stock_id]['StockStateName']
            
            # 33: on sale, 34: out of stock, 36: pre-sell
            return stock_stat, stock_stat_name

        except Exception as e:
            print('Exception:', e)
            time.sleep(5)

        return 0, ''
    
    def good_detail(self, stock_id, area_id=None):
        # return good detail
        good_data = {
            'id': stock_id,
            'name': '',
            'link': '',
            'price': '',
            'stock': '',
            'stockName': '',
        }
        
        try:
            # shop page
            stock_link = 'http://item.jd.com/{0}.html'.format(stock_id)
            resp = self.sess.get(stock_link)

            # good page
            soup = bs4.BeautifulSoup(resp.text, "html.parser")
            print(soup.prettify())
            
            # good name
            tags = soup.select('div#name h1')
            if len(tags) == 0:
                tags = soup.select('div.sku-name')
            good_data['name'] = tags_val(tags).strip(' \t\r\n')

            # direct add to cart link
            tags = soup.select('a#InitCartUrl')
            link = tags_val(tags, key='href')
            
            if link[:2] == '//':
                link = 'http:' + link
            good_data['link'] = link
        
        except Exception as e:
            print(e)

        # good price
        good_data['price'] = self.good_price(stock_id)
        
        # good stock
        good_data['stock'], good_data['stockName'] = self.good_stock(stock_id=stock_id, area_id=area_id)
        # stock_str = u'有货' if good_data['stock'] == 33 else u'无货'
        
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('{0} > 商品详情'.format(time.ctime()))
        print('编号：{0}'.format(good_data['id']))
        print('库存：{0}'.format(good_data['stockName']))
        print('价格：{0}'.format(good_data['price']))
        print('名称：{0}'.format(good_data['name']))
        print('链接：{0}'.format(good_data['link']))
        
        return good_data        

    def good_price(self, stock_id):
        # get good price
        url = 'http://p.3.cn/prices/mgets'
        payload = {
            'type': 1,
            'pduid': int(time.time() * 1000),
            'skuIds': 'J_' + stock_id,
        }
        
        price = '?'
        try:
            resp = self.sess.get(url, params=payload)
            resp_txt = resp.text.strip()
            # print(resp_txt)

            js = json.loads(resp_txt[1:-1])
            # print('价格', 'P: {0}, M: {1}'.format(js['p'], js['m'])
            price = js.get('p')

        except Exception as e:
            print(e)

        return price

    def buy(self, options):
        # stock detail
        good_data = self.good_detail(options.good)

        # retry until stock not empty
        if good_data['stock'] != 33:
            # flush stock state
            while good_data['stock'] != 33 and options.flush:
                print('<%s> <%s>' % (good_data['stockName'], good_data['name']))
                time.sleep(options.wait / 1000.0)
                good_data['stock'], good_data['stockName'] = \
                    self.good_stock(stock_id=options.good, area_id=options.area)
                
            # retry detail
            # good_data = self.good_detail(options.good)

        # failed 
        link = good_data['link']
        if good_data['stock'] != 33 or link == '':
            # print('stock {0}, link {1}'.format(good_data['stock'], link)
            return False

        try:
            # add to cart
            resp = self.sess.get(link, cookies=self.cookies)
            soup = bs4.BeautifulSoup(resp.text, "html.parser")

            # tag if add to cart succeed
            tag = soup.select('h3.ftx-02')
            if tag is None:
                tag = soup.select('div.p-name a')

            if tag is None or len(tag) == 0:
                print('添加到购物车失败')
                return False
            
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print('{0} > 购买详情'.format(time.ctime()))
            print('结果：{0}'.format(tags_val(tag)))

            # change count
            self.buy_good_count(options.good, options.count)
            
        except Exception as e:
            print(e)
        else:
            self.cart_detail()
            return self.submit_order(options.submit)

        return False

    def buy_good_count(self, good_id, count):
        url = 'http://cart.jd.com/changeNum.action'

        payload = {
            'venderId': '8888',
            'pid': good_id,
            'pcount': count,
            'ptype': '1',
            'targetId': '0',
            'promoID': '0',
            'outSkus': '',
            'random': random.random(),
            'locationId': '22_1930_50945_52160',  # need changed to your area location id
        }

        try:
            rs = self.sess.post(url, params=payload, cookies=self.cookies)
            if rs.status_code == 200:
                js = json.loads(rs.text)
                if js.get('pcount'):
                    print('数量：%s @ %s' % (js['pcount'], js['pid']))
                    return True
            else:
                print('购买 %d 失败' % count)
                
        except Exception as e:
            print(e)

        return False
        
    def cart_detail(self):
        # list all goods detail in cart
        cart_url = 'https://cart.jd.com/cart.action'
        cart_header = '购买    数量    价格        总价        商品'
        cart_format = '{0:8}{1:8}{2:12}{3:12}{4}'
        
        try:	
            # resp = self.sess.get(cart_url, cookies=self.cookies)
            resp = self.sess.get(cart_url, cookies=self.cookies)
            resp.encoding = 'utf-8'
            soup = bs4.BeautifulSoup(resp.text, "html.parser")
            # print(soup.prettify())
            
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print('{0} > 购物车明细'.format(time.ctime()))
            print(cart_header)
            
            for item in soup.select('div.item-form'):
                check = tags_val(item.select('div.cart-checkbox input'), key='checked')
                check = ' + ' if check else ' - '
                count = tags_val(item.select('div.quantity-form input'), key='value')
                price = tags_val(item.select('div.p-price strong'))		
                sums = tags_val(item.select('div.p-sum strong'))
                gname = tags_val(item.select('div.p-name a'))
                #: ￥字符解析出错, 输出忽略￥
                print(cart_format.format(check, count, price[1:], sums[1:], gname))

            t_count = tags_val(soup.select('div.amount-sum em'))
            t_value = tags_val(soup.select('span.sumPrice em'))
            print('总数: {0}'.format(t_count))
            print('总额: {0}'.format(t_value[1:]))

        except Exception as e:
            print(e)

    def submit_order(self, submit=False):
        # get order info detail, and submit order
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('{0} > 订单详情'.format(time.ctime()))

        pre_submit_url = 'http://trade.jd.com/shopping/order/getOrderInfo.action'
        payload = {
            'rid': str(int(time.time() * 1000)),
        }

        # get pre_submit_url page(从购物车提交订单流程：1.我的购物车 2.填写核对订单信息 3.成功提交订单)
        # order_url是第2步的请求地址，会自动带入购物车中已勾选的商品
        rs = self.sess.get(pre_submit_url, params=payload, cookies=self.cookies)
        soup = bs4.BeautifulSoup(rs.text, "html.parser")
        # print(soup.prettify())

        # order summary
        payment = tag_val(soup.find(id='sumPayPriceId'))
        detail = soup.find(class_='fc-consignee-info')

        if detail:
            snd_usr = tag_val(detail.find(id='sendMobile'))
            snd_add = tag_val(detail.find(id='sendAddr'))

            print('应付款：{0}'.format(payment))
            print(snd_usr)
            print(snd_add)

        # just test, not real order
        if not submit:
            return False

        # order info(因为使用京豆需要输入支付密码，这里无法使用)
        payload = {
            'overseaPurchaseCookies': '',
            'submitOrderParam.sopNotPutInvoice': 'false',
            'submitOrderParam.trackID': self.trackid,
            'ebf': '2',
            'submitOrderParam.ignorePriceChange': '0',
            'submitOrderParam.btSupport': '0',
            'submitOrderParam.eid': self.eid,
            'submitOrderParam.fp': self.fp,
            # GET /shopping/order/getEasyOrderInfo.action?rid=1499757151538 HTTP/1.1, trade.jd.com
            # <input type="hidden" id="riskControl" value=""/>
            'riskControl': 'D0E404CB705B97320BB6800AA45CEC1066B7DE36B44D41A5F3FA34DC5DA0A375C6A580BF03771F3D',
            'submitOrderParam.isBestCoupon': '1'
        }

        order_url = 'http://trade.jd.com/shopping/order/submitOrder.action'
        rp = self.sess.post(order_url, params=payload, cookies=self.cookies)

        if rp.status_code == 200:
            js = json.loads(rp.text)
            if js['success'] is True:
                print('下单成功！订单号：{0}'.format(js['orderId']))
                print('请前往东京官方商城付款')
                return True
            else:
                print('下单失败！<{0}: {1}>'.format(js['resultCode'], js['message']))

    def easy_buy(self, good_id):

        easy_buy_url = 'http://easybuy.jd.com/skuDetail/newSubmitEasybuyOrder.action'
        pay_load = {
            'callback': 'easybuysubmit',
            'skuId': good_id,
            'num': 1,
            'gids': '',
            'ybIds': '',
            'did': '',
            '_': int(time.time() * 1000)
        }
        rp = self.sess.get(easy_buy_url, params=pay_load, headers=self.headers, cookies=self.cookies)
        print(rp)
        print(rp.status_code)

        # if rp.status_code == 200:
        #     start = rp.text.find('(')
        #     end = rp.text.find(')')
        #     js = json.loads(rp.text[start+1:end])
        #     if js['success'] is True:
        #         order_id = js['jumpUrl'].split('=')[-1]
        #         print('下单成功！订单号：{0}'.format(order_id))
        #         print('请前往东京官方商城付款')
        #         return True
        #     else:
        #         print('下单失败！<{0}: {1}>'.format(js['resultCode'], js['message']))


def main(options):
    jd = JDWrapper()
    if not jd.check_cookies():
        return

    while not jd.buy(options) and options.flush:
        time.sleep(options.wait / 1000.0)


# if __name__ == '__main__':
#     # help message
#     parser = argparse.ArgumentParser(description='Simulate to login Jing Dong, and buy specified good')
#     # parser.add_argument('-u', '--username',
#     # help='Jing Dong login user name', default='')
#     # parser.add_argument('-p', '--password',
#     # help='Jing Dong login user password', default='')
#     parser.add_argument('-a', '--area',
#                         help='Area string, like: 1_72_2799_0 for Beijing', default='22_1930_50945_52160')
#     parser.add_argument('-g', '--good',
#                         help='Jing Dong good ID', default='')
#     parser.add_argument('-c', '--count', type=int,
#                         help='The count to buy', default=1)
#     parser.add_argument('-w', '--wait', type=int, default=500,
#                         help='Flush time interval, the unit is ms')
#     parser.add_argument('-f', '--flush', action='store_true',
#                         help='Continue flush if good out of stock')
#     parser.add_argument('-s', '--submit', action='store_true',
#                         help='Submit the order to Jing Dong')
#
#     # example goods
#     mi_zone = '1044706'
#     iphone_7 = '3133851'
#     apple = '11548341923'
#
#     buy_options = parser.parse_args()
#     print(buy_options)
#
#     # for test
#     if buy_options.good == '':
#         buy_options.good = apple
#
#     main(buy_options)

demo = JDWrapper()
# print(demo.load_cookies('jd_cookies'))
# demo.good_detail('11548341923', '22_1930_50945_52160')
# demo.login_by_qr()
# demo.save_cookies(demo.login_by_qr(), 'jd_cookies')
demo.check_cookies()
# demo.cart_detail()
# demo.easy_buy('1044706')
# pprint.pprint(demo.load_cookies('jd_cookies'))
# demo.submit_order()
