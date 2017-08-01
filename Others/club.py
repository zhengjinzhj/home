#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import csv
from bs4 import BeautifulSoup


def get_info():
    base_url = 'http://www.108j.club/category/'
    end_urls = ['korea', 'korea/page/2', 'western',
               'western/page/2', 'japan', 'japan/page/2', 'vr']
    all_data = []
    for end_url in end_urls:
        url = base_url + end_url
        if end_url[:5] == 'korea':
            category = '韩系'
        elif end_url[:7] == 'western':
            category = '欧美'
        elif end_url[:5] == 'japan':
            category = '日系'
        else:
            category = 'VR'
        print('**************** Crawling: %s *****************' % url)
        content = requests.get(url)
        soup = BeautifulSoup(content.text, 'html.parser')
        for item in soup.find('ul', class_='update_area_lists').find_all('a'):
            row = list([category])
            row.append(item['title'])
            row.append(item['href'])
            all_data.append(row)
    return all_data  # 返回一个二级列表


def write_file(all_data):
    with open('108tv.csv', 'w', encoding='utf-8', newline='') as csv_file:
        csv_write = csv.writer(csv_file, dialect='excel')
        csv_write.writerow(['category', 'title', 'link'])
        for row in all_data:
            csv_write.writerow(row)
    csv_file.close()


def get_page_urls(all_data):
    page_urls = set()
    for row in all_data:
        page_url = row[2]
        page_urls.add(page_url)
    return page_urls


def get_pic_urls(page_urls):
    base_url = 'http://www.108j.club/pic/'
    pic_urls = set()
    for page_url in page_urls:
        page_no = page_url.split('/')[-1][:-5]
<<<<<<< HEAD
        for i in range(1, 7):
=======
        for i in range(1, 9):
>>>>>>> 0db49f99df09bbe78cf278fd467facc8e538ae6a
            pic_url = base_url + page_no + '/' + str(i) + '.jpg'
            pic_urls.add(pic_url)
    return pic_urls


# pp = get_page_urls(get_info())
# print(get_pic_urls(pp))
