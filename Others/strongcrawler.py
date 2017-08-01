# -*- coding:utf-8 -*-

import re
import requests
import random
import time


class Download(object):

    def __init__(self):
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 "
            "Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 "
            "Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 "
            "Safari/535.24"
        ]
        self.ip_list = []
        html = requests.get('http://haoip.cc/tiqu.htm')
        ips = re.findall('r/>(.*?)<b', html.text, re.S)
        for ip in ips:
            self.ip_list.append(ip.strip())

    def get(self, url, timeout, proxy=None, retry_num=6):
        user_agent = random.choice(self.user_agent_list)
        headers = {'User-Agent': user_agent}
        if proxy is None:
            try:
                response = requests.get(url, headers=headers)
                return response
            except:
                if retry_num > 0:
                    time.sleep(10)
                    print '获取网页失败，10秒后将尝试倒数第%d次获取' % retry_num
                    return self.get(url, timeout, retry_num-1)
                else:
                    print '开始使用代理'
                    time.sleep(10)
                    ip = random.choice(self.ip_list)
                    proxy = {'http': ip}
                    return self.get(url, timeout, proxy,)
        else:
            try:
                ip = random.choice(self.ip_list)
                proxy = {'http': ip}
                response = requests.get(url, headers=headers, proxies=proxy, timeout=timeout)
                return response
            except:
                if retry_num > 0:
                    time.sleep(10)
                    ip = random.choice(self.ip_list)
                    print '获取网页失败，换一个代理，10秒后将尝试倒数第%d次获取' % retry_num
                    print '当前的代理地址为：%s' % ip
                    return self.get(url, timeout, proxy, retry_num-1)
                else:
                    print '代理也不好使了，取消代理'
                    return self.get(url, 3)  # timeout=3

request = Download()





