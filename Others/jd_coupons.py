#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests
import datetime
import pickle

logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)

# log format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# console log
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


user_agent = ('User-Agent:Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) '
              'AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5')
session = requests.session()
session.headers['User-Agent'] = user_agent


def get_cookie():
    with open('jd_cookies', 'rb') as f:
        return pickle.load(f)


def get_coupon():
    timer = '2017-07-17 16:18'  # 抢券时间
    # 抢券url
    coupon_url30 = 'https://coupon.m.jd.com/coupons/show.action?key=8325f746b1d341de8e0d179e418cb119&roleId=6729291&to=sale.jd.com/m/act/ZFMnErV8z0tAGxs1.html'
    # 抢券referer
    # referer = 'https://coupon.m.jd.com/coupons/show.action?key=8325f746b1d341de8e0d179e418cb119&roleId=6729291&to=sale.jd.com/m/act/ZFMnErV8z0tAGxs1.html'
    test = 'https://sale.jd.com/act/4dXklOqfC5L.html'
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        if now == timer:
            cookies = get_cookie()
            # session.cookies = requests.utils.cookiejar_from_dict(get_cookie())
            for url in (coupon_url30, ):
                resp = session.get(url=url, headers={'Referer': test, }, cookies=cookies)
                logger.info(resp.text)
            break


if __name__ == '__main__':
    get_coupon()

