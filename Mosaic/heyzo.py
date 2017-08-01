# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import requests
import os


# http://sample.heyzo.com/contents/3000/1313/heyzo_hd_1313_sample.mp4
# http://sample.heyzo.com/contents/3000/0001/sample.mp4
class Heyzo(object):

    def __init__(self):
        self.proxy = {'http': '127.0.0.1:1080'}
        self.base_url = 'http://www.heyzo.com/listpages/all_'

    def get_total_page_and_latest_video(self):
        # f1 = open('heyzo.html', 'w+')
        first_page = self.base_url + '1.html'
        data = requests.get(first_page, proxies=self.proxy)
        html = data.text.encode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # print >>f1, soup.prettify().encode('utf-8')
        total_page_part = soup.select('.list_pagetotal')
        total_page = int(total_page_part[0].string)
        latest_part = soup.find(class_='movie movie358').contents[1]
        temp = latest_part['href'].split('/')
        latest_video = int(temp[-2])
        return [total_page, latest_video]

    def get_one_page(self, page_no):
        page_url = self.base_url + str(page_no) + '.html'
        data = requests.get(page_url, proxies=self.proxy)
        html = data.text.encode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # print soup.find(id='movies')
        for item in soup.select('div[class="movie movie358"]'):
            for title in item.select('.movietitle'):
                print(title.string.strip())
                print(title['href'])
            for actor in item.select('.actor'):
                print(actor.string.strip())

    @staticmethod
    def make_folder(folder_name):
        if not os.path.exists(folder_name):
            print('Creating folder "' + folder_name + '"...')
            os.mkdir(folder_name)
        else:
            print('Folder "' + folder_name + '" already exists, skip...')

    def save_img(self):
        self.make_folder('heyzo')
        # latest_video = self.get_total_page_and_latest_video()[1]
        former_part = 'http://www.heyzo.com/contents/3000/'
        back_part = '/images/player_thumbnail.jpg'
        for video_no in range(1313, 1533):
            if video_no < 10:
                video_no = '000' + str(video_no)
            elif video_no < 100:
                video_no = '00' + str(video_no)
            elif video_no < 1000:
                video_no = '0' + str(video_no)
            else:
                video_no = str(video_no)
            img_name = video_no + '.jpg'
            img_location = 'heyzo' + '/' + img_name
            if not os.path.isfile(img_location):
                print('Downloading ' + img_name)
                img_url = former_part + video_no + back_part
                data = requests.get(img_url, proxies=self.proxy)
                data = data.content
                pic = open(img_location, 'wb')
                pic.write(data)
                pic.close()
            else:
                print(img_name + ' already exists, skip...')


demo = Heyzo()
# demo.get_total_page_and_latest_video()
# demo.get_one_page(1)
demo.save_img()

