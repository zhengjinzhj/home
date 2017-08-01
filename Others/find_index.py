# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv


def get_contents():
    base_url = 'http://www.ftoow.com/thread.php?fid-225-page-'  # TGod original albums
    total_page = get_total_page(base_url)
    csv_file = file('MiStar.csv', 'wb')
    csv_writer = csv.writer(csv_file, dialect='excel')
    csv_writer.writerow(['Title'])
    for page in range(1, total_page+1):
        url = base_url + str(page) + '.html'
        print 'Crawling page: %d' % page
        response = requests.get(url)
        response.encoding = 'gbk'
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('a', class_='subject_t')
        for item in items:
            title = [item.string]
            csv_writer.writerow(title)
    csv_file.close()


def get_total_page(base_url):
    first_url = base_url + '1.html'
    source = requests.get(first_url)
    soup = BeautifulSoup(source.content.decode('gbk'), 'html.parser')
    # print soup.prettify()
    item = soup.find('div', class_='pages').find_all('a')[-1]
    total_page = str(item.string.strip())
    if '.' in item.string:
        total_page = total_page.replace('.', '')
    return int(total_page)

get_contents()
