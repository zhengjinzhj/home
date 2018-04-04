# -*- coding:utf-8 -*-

import csv
import requests
import os


def make_folder(location, folder):
    # make folder and switch to the directory
    directory = os.path.join(location, folder.strip())
    if not os.path.exists(directory):
        print('Creating directory: %s' % directory)
        os.makedirs(directory)
        os.chdir(directory)  # Switch to the directory
        return os.getcwd()  # Return current directory
    else:
        print('%s is already exists, skip...' % directory)
        os.chdir(directory)
        return os.getcwd()


def save_photo(photo_link, photo_format='', link_index=0, back_index=0):
    # for link like http://www.test.com/image.jpg format
    if photo_format == '':
        photo_name = photo_link.split('/').pop()
    # for link like http://images-eds.xboxlive.com/image?url=z951ykbFvR2Ec.wW11 format
    elif link_index != 0:
        photo_name = str(link_index) + photo_format
    # for link like http://www.test.com/moviepages/031817_501/images/str.jpg format
    else:
        split_link = photo_link.split('/')
        photo_name = split_link[back_index] + photo_format
    if not os.path.isfile(photo_name):
        print('Downloading photo %s' % photo_name)
        data = requests.get(photo_link).content
        photo = open(photo_name, 'wb')
        photo.write(data)
        photo.close()
    else:
        print('Photo %s already exists, skip...' % photo_name)


def main(csv_file_name):
    make_folder('D:\Download', 'forza')
    with open(csv_file_name, encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        photo_links = [row['Image Url'] for row in reader]
        for i in range(204, len(photo_links)):
            link = photo_links[i]
            # split_link = link.split('/')
            # split_link.pop()
            # split_link.pop()
            # picture_id = split_link.pop()
            save_photo(link, photo_format='.png', link_index=i+1)
    #     picture_id = [row['MovieID'] for row in data]
    # link_id = dict(zip(picture_link, picture_id))
    # # print link_id
    # make_folder('1pondo')
    # for (k, v) in link_id.items():
    #     # print 'dict[%s]=' % k, v
    #     save_img(k, v)

main('C:\\Users\\Administrator\\PycharmProjects\\home\\Others\\achievements.csv')

