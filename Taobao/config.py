# -*- coding:utf-8 -*-

from selenium import webdriver

URL_FILE = 'urls.txt'
OUT_FILE = 'result.xls'
COUNT_FILE = 'count.txt'

DRIVER = webdriver.Chrome()

TIMEOUT = 30
MAX_SCROLL_TIME = 10
TOTAL_URLS_COUNT = 0
NOW_URL_COUNT = 0

LOGIN_URL = 'https://login.taobao.com/member/login.jhtml'

SEARCH_LINK = 'https://www.tmall.com/?spm=a220m.1000858.a2226n0.1.NRh3jA'

CONTENT = ''

PAGE = 25
FILTER_SHOP = False

USERNAME = 'zhengjin0706'
PASSWORD = 'Naobing123'
