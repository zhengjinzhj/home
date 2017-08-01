# -*- coding:utf-8 -*-

import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
import config
import write_to_excel
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery


def scroll_bottom_recommends(driver, count):
    print '正在尝试第%d次下拉' % count
    try:
        js = 'window.scrollTo(0, document.body.scrollHeight-' + str(count*count*100) + ')'
        driver.execute_script(js)
    except WebDriverException:
        print '下拉寻找橱窗宝贝时出现问题'
    time.sleep(2)
    try:
        driver.find_element_by_css_selector('#J_TjWaterfall li')
    except NoSuchElementException:
        return False
    return True


def is_recommends_appear(driver, max_time=10):
    count = 1
    result = scroll_bottom_recommends(driver, count)
    while not result:
        count += 1
        result = scroll_bottom_recommends(driver, count)
        if count == max_time:
            return False
    return True


def scrap_recommends_page(url):
    print '开始寻找下方橱窗推荐宝贝', url
    driver = config.DRIVER
    timeout = config.TIMEOUT
    max_scroll_time = config.MAX_SCROLL_TIME
    try:
        driver.get(url)
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, 'J_TabBarBox'))
        )
    except TimeoutException:
        return False
    if is_recommends_appear(driver, max_scroll_time):
        print '已经成功加载出下方橱窗推荐宝贝信息'
        return driver.page_source
    else:
        return False


def get_recommends_info(url):
    info = []
    if not url.startswith('http'):
        url = 'https:' + url
    html = scrap_recommends_page(url)
    if html:
        doc = PyQuery(html)
        items = doc('#J_TjWaterfall > li')
        print '分析得到下方宝贝中的用户评论:'
        for item in items.items():
            url = item.find('a').attr('href')
            if not url.startswith('http'):
                url = 'https:' + url
            comments_info = []
            comments = item.find('p').items()
            for comment in comments:
                comment_user = comment.find('b').remove().text()
                comment_content = comment.text()
                # anonymous_str = config.ANONYMOUS_STR
                comments_info.append((comment_content, comment_user))
            info.append({'url': url, 'comments_info': comments_info})
        return info
    else:
        print '抓取网页失败，跳过'
        return []


def deal_recommends_info(url):
    infos = get_recommends_info(url)
    for info in infos:
        url = info.get('url')
        comments_info = info.get('comments_info')
        for comment_info in comments_info:
            comment_content = comment_info[0]
            comment_user = comment_info[1]
            print 'comment_user', comment_user
            if len(comments_info) > 0 and not write_to_excel.repeat_excel(comment_user):
                write_to_excel.write_info((comment_user, comment_content, url))

























