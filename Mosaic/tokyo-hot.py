# -*- coding:utf-8 -*-

import re
import csv
import requests
import os


# http://my.cdn.tokyo-hot.com/media/samples/6081.mp4
# http://www.tokyo-hot.com/product/6389/
class TokyoHot(object):

    def __init__(self):
        self.proxy = {'http': '127.0.0.1:8087', 'https': '127.0.0.1:8087'}
        self.main_url = 'http://www.tokyo-hot.com/product/?page='
        self.parameter = {'filter': '撮りおろし徹底陵辱ビデオ', 'type': 'genre'}

    def get_total_page(self):
        first_url = self.main_url + str(1)
        data = requests.get(first_url, params=self.parameter, proxies=self.proxy)
        content = data.text
        content = re.sub('"', '', content)
        total_page = re.findall('<p.*?naviend><a href=\?page=(.*?)&amp', content)
        return int(total_page[0])

    def get_page_content(self, page_no):
        contents = []
        page_url = self.main_url + str(page_no)
        data = requests.get(page_url, params=self.parameter, proxies=self.proxy)
        response = data.text.encode('utf-8')
        response = re.sub('"', '', response)
        pattern = re.compile('<li class=detail>.*?<a href=\/product\/(.*?)\/.*?src=(.*?) alt.*?'
                             '<div class=title>(.*?)</div>.*?<div class=actor>(.*?)\(作品番号:(.*?)\)', re.S)
        items = re.findall(pattern, response)
        for item in items:
            # print item[1]
            contents.append([item[0], item[1], item[2], item[3], item[4]])
        return contents

    def save_into_csv(self):
        print 'Now Crawling page contents...'
        csv_file = file('tokyohot.csv', 'wb')
        writer = csv.writer(csv_file, dialect='excel')
        writer.writerow(['Movie ID', 'Series No', 'Title', 'Actress', 'Thumbnail'])
        for page in xrange(1, self.get_total_page()+1):
            print '*'*20 + 'PAGE ' + str(page) + '*'*20
            contents = self.get_page_content(page)
            for item in contents:
                thumbnail = item[1].replace('220x124', '820x462')
                thumbnail = re.sub('-0\d+', '', thumbnail)
                actress = item[3].strip()
                series_no = item[4].strip()
                writer.writerow([item[0], series_no, item[2], actress, thumbnail])
        csv_file.close()

    @staticmethod
    def make_folder(folder_name):
        if not os.path.exists(folder_name):
            print 'Making folder "' + folder_name + '"'
            os.mkdir(folder_name)
        else:
            print 'Folder "' + folder_name + '" already exists, skip...'

    def save_img(self, thumbnail, series_no):
        file_name = series_no + '.jpg'
        file_location = 'tokyohot' + '/' + file_name
        if not os.path.isfile(file_location):
            print 'Downloading ' + file_name
            data = requests.get(thumbnail, proxies=self.proxy)
            data = data.content
            thumbnail = open(file_location, 'wb')
            thumbnail.write(data)
            thumbnail.close()
        else:
            print file_name + ' already exists, skip'

    def download_thumbnails(self):
        self.make_folder('tokyohot')
        with open('tokyohot.csv', 'rb') as csv_file:
            reader = csv.DictReader(csv_file)
            data = [row for row in reader]
            thumbnail_url = [row['Thumbnail'] for row in data]
            series_no = [row['Series No'] for row in data]
            url_name = dict(zip(thumbnail_url, series_no))
            for (url, file_name) in url_name.items():
                self.save_img(url, file_name)

demo = TokyoHot()
# print demo.get_total_page()
demo.save_into_csv()
# demo.download_thumbnails()








