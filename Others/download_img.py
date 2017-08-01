# -*- coding:utf-8 -*-

import csv
import urllib2
import os

proxy = urllib2.ProxyHandler({'http': '127.0.0.1:8087'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)


def make_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def save_img(picture_link, picture_id):
    file_name = picture_id + '.jpg'
    full_location = '1pondo' + '/' + file_name
    if not os.path.isfile(full_location):
        print 'Downloading ' + file_name
        content = opener.open(picture_link)
        data = content.read()
        pic = open(full_location, 'wb')
        pic.write(data)
        pic.close()
    else:
        print file_name + ' is already exits.'


def main():
    with open('1pondo.csv', 'rb') as csv_file:
        reader = csv.DictReader(csv_file)
        data = [row for row in reader]
        picture_link = [row['Thumbnail'] for row in data]
        for link in picture_link:
            split_link = link.split('/')
            split_link.pop()
            split_link.pop()
            picture_id = split_link.pop()
            save_img(link, picture_id)
    #     picture_id = [row['MovieID'] for row in data]
    # link_id = dict(zip(picture_link, picture_id))
    # # print link_id
    # make_folder('1pondo')
    # for (k, v) in link_id.items():
    #     # print 'dict[%s]=' % k, v
    #     save_img(k, v)

main()

