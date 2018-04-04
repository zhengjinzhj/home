# -*- coding: utf-8 -*-

import requests
from lxml import etree
from multiprocessing import Pool
import os


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}


def download(title, url, filename):
    r1 = requests.get(url, headers=headers).text
    h1 = etree.HTML(r1)
    pages = h1.xpath('//div//p/text()')[2:]
    with open(filename, 'a') as f:
        f.write(title + '\n')
    for page in pages:
        with open(filename, 'a') as f:
            f.write(page + '\n')


def main(url):
    start_url = 'http://www.jinyongwang.com' + url
    print(start_url)
    s_name = start_url.split('/')[-2]
    if s_name.startswith('o'):
        folder = 'old/'
        if not os.path.exists(folder):
            os.makedirs(folder)
    elif s_name.startswith('n'):
        folder = 'new/'
        if not os.path.exists(folder):
            os.makedirs(folder)
    else:
        folder = 'now/'
        if not os.path.exists(folder):
            os.makedirs(folder)
    filename = folder + s_name + '.txt'
    base_url = 'http://www.jinyongwang.com'
    r2 = requests.get(start_url, headers=headers).text
    h2 = etree.HTML(r2)
    urls2 = h2.xpath('//ul[@class="mlist"]/li/a/@href')
    titles = h2.xpath('//ul[@class="mlist"]/li//text()')
    for index, url in enumerate(urls2):
        full_url = base_url + url
        title = titles[index]
        download(title, full_url, filename)


if __name__ == '__main__':
    url01 = 'http://www.jinyongwang.com/'
    response = requests.get(url01, headers=headers).text
    html = etree.HTML(response)
    urls = html.xpath('//li[@class="book_li"]/p[3]//a/@href')
    pool = Pool()
    pool.map(main, urls)
    pool.close()
    pool.join()
