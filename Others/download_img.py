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


def st_downloader(link_id_pair):
    url = link_id_pair[0]
    file_name = link_id_pair[1] + '.' + url.split('.')[-1]
    if not os.path.isfile(file_name):
        print('Downloading %s' % file_name)
        response = requests.get(url)
        file = open(file_name, 'wb')
        file.write(response.content)
        file.close()
    else:
        print('%s already exists, skip...' % file_name)


def get_link_id_pair(csv_file, url_line, id_line):
    with open(csv_file, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        data = [row for row in reader]
        picture_link = [row[url_line] for row in data]
        picture_id = [row[id_line] for row in data]
        link_id_pair = dict(zip(picture_link, picture_id))
        return link_id_pair


def main(csv_file_name):
    make_folder('D:\Download', 'forza')
    with open(csv_file_name, encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        links = [row['Image Url'] for row in reader]
        for i in range(204, len(links)):
            link = links[i]
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
