# -*- coding:utf-8 -*-

import config
import get_recommands
import re
import write_to_excel
import time


def scrap(url):
    get_recommands.deal_recommends_info(url)


def get_urls():
    try:
        file = open(config.URL_FILE, 'r')
        content = file.read()
        pattern = re.compile('(.*?//.*?)\s', re.S)
        urls = re.findall(pattern, content)
        return urls
    except Exception, e:
        print '获取链接失败', e.message


def log_in():
    driver = config.DRIVER
    driver.get(config.LOGIN_URL)
    driver.find_element_by_class_name('login-switch').click()
    username = driver.find_element_by_id('TPL_username_1')
    username.send_keys(config.USERNAME)
    password = driver.find_element_by_name('TPL_password')
    password.send_keys(config.PASSWORD)
    driver.find_element_by_id('J_SubmitStatic').click()
    time.sleep(3)
    if config.USERNAME in driver.page_source:
        return True
    else:
        return False


def from_input():
    print '请输入宝贝链接'
    url = raw_input()
    # driver = config.DRIVER
    # driver.get(config.LOGIN_URL)
    # print '完成登录之后，请输入任意键，开始执行爬取'
    # raw_input()
    if log_in():
        scrap(url)
        print '采集结束'
    else:
        print '登录失败，请检查用户名和密码！'


def from_file():
    driver = config.DRIVER
    driver.get(config.LOGIN_URL)
    print '完成登录之后，请输入任意键，开始执行爬取'
    raw_input()
    urls = get_urls()
    config.TOTAL_URLS_COUNT = len(urls)
    print '共有%d个链接' % config.TOTAL_URLS_COUNT
    count = int(write_to_excel.get_count())
    print '上次爬取到第%d个链接' % count
    print '输入 1 继续爬取， 输入 2 重新爬取：'
    num = raw_input()
    if num == '2':
        count = 0
        print '开始重新爬取'
    if count < config.TOTAL_URLS_COUNT:
        for count in xrange(count, config.TOTAL_URLS_COUNT):
            write_to_excel.write_count(count, config.COUNT_FILE)
            url = urls[count]
            print '正在爬取第%d个网页, 共%d个' % (count+1, config.TOTAL_URLS_COUNT)
            config.NOW_URL_COUNT = count
            scrap(url)
            count += 1
            print '当前已完成采集%d个, 共%d个' % (config.NOW_URL_COUNT, config.TOTAL_URLS_COUNT)
        print '采集结束,完成了%d个链接的采集' % len(urls)
    else:
        print '链接上次已经全部爬取完毕'

# log_in()
from_input()
# from_file()
# https://detail.tmall.com/item.htm?id=525605563072
# https://item.taobao.com/item.htm?id=535779169052


























