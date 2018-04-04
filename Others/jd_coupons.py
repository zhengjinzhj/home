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
        f.seek(0)
        return pickle.load(f)


def get_coupon():
    timer = '2017-08-18 10:55'  # 抢券时间
    # 抢券url
    coupon = 'https://coupon.m.jd.com/coupons/show.action?key=65cc9ad745054e14b306e2e8869a97e2&roleId=7750015&to=sale.jd.com/m/act/aTFoJ8hwCdcnri.html'
    # 抢券referer
    referer = 'https://sale.jd.com/m/act/aTFoJ8hwCdcnri.html'
    # test = 'https://sale.jd.com/act/aTFoJ8hwCdcnri.html'
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        if now == timer:
            cookies = get_cookie()
            # session.cookies = requests.utils.cookiejar_from_dict(get_cookie())
            for url in (coupon, ):
                resp = session.get(url=url, headers={'Referer': referer, }, cookies=cookies)
                logger.info(resp.text)
            break


if __name__ == '__main__':
    get_coupon()

