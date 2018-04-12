# -*- coding:utf-8 -*-

import csv
import requests
import os
import time
from multiprocessing import Pool


heyzo_pattern = 'http://www.heyzo.com/contents/3000/{:04d}/images/player_thumbnail.jpg'
heydouga_pattern = 'http://image01.heydouga.com/contents/4030/{:04d}/player_thumb.jpg'
ssr_proxy = {'http': '127.0.0.1:1080', 'https': '127.0.0.1:1080'}


def make_folder(destination):
    # make folders and switch to the destination
    if not os.path.exists(destination):
        print('Creating destination: %s' % destination)
        os.makedirs(destination)
        os.chdir(destination)  # Switch to the destination
        return os.getcwd()  # Return current destination
    else:
        print('%s is already exists, skip...' % destination)
        os.chdir(destination)
        return os.getcwd()


def st_downloader(link_id_pair):
    # Not really a link&id pair, only link
    if isinstance(link_id_pair, str):
        url = link_id_pair
        # for heyzo.com and heydouga.com
        # http://www.heyzo.com/contents/3000/2050/images/player_thumbnail.jpg
        # http://image01.heydouga.com/contents/4030/789/player_thumb.jpg
        if 'heyzo' in link_id_pair:
            file_name = url.split('/')[-3] + '.jpg'
        elif 'heydouga' in link_id_pair:
            file_name = url.split('/')[-2] + '.jpg'
        else:
            file_name = url.split('/')[-1]
    else:
        url = link_id_pair[0]
        file_name = link_id_pair[1] + '.' + url.split('.')[-1]
    if not os.path.isfile(file_name):
        response = requests.get(url, proxies=ssr_proxy)
        file = open(file_name, 'wb')
        file.write(response.content)
        print('%s: downloading %s' % (get_time(), file_name))
        file.close()
    else:
        print('%s: %s already exists, skip...' % (get_time(), file_name))


def get_time():
    return time.strftime('%H:%M:%S', time.localtime())


def get_link_id_pair(csv_file, url_line, id_line):
    with open(csv_file, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        data = [row for row in reader]
        picture_link = [row[url_line] for row in data]
        picture_id = [row[id_line] for row in data]
        link_id_pair = zip(picture_link, picture_id)
        return link_id_pair


def make_batch_link(pattern, start, end):
    # pattern like: http://i.meizitu.net/2018/03/32b{:02d}.jpg
    return [pattern.format(f) for f in range(start, end+1)]


def main(destination, csv_file='', url_line='', id_line='', pattern='', start=0, end=0):
    make_folder(destination)
    pool = Pool()
    if csv_file != '':
        link_id_pairs = get_link_id_pair(csv_file, url_line, id_line)
    elif pattern != '':
        link_id_pairs = make_batch_link(pattern, start, end)
    else:
        print('Please provide csv_file with link&id lines or batch link pattern with start&end number')
        link_id_pairs = []
    pool.map(st_downloader, link_id_pairs)
    pool.close()
    pool.join()


if __name__ == '__main__':
    main('D:\Download\des', csv_file='carib_newest.csv', url_line='Thumbnail', id_line='Movie ID')
    # main('D:\Download\des', pattern=heyzo_pattern, start=899, end=1200)
