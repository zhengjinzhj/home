#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import csv
import requests


class TaobaoMM(object):
    site_url = 'https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8&pageSize=100&currentPage='

    def get_page(self, page_index):
        # Get the given page's (index page) page source and do some small 'formatted'.
        url = TaobaoMM.site_url + str(page_index)
        response = requests.get(url).text
        source_data = self.remove_double_quotation_marks(response)
        return source_data

    def get_contents(self, page_index):
        # Get the wanted data from given page source (index page).
        source_data = self.get_page(page_index)
        pattern = re.compile('\{avatarUrl:(.*?),cardUrl:(.*?),city:(.*?),.*?,identityUrl.*?realName:(.*?),'
                             'totalFanNum:(.*?),totalFavorNum:(.*?),userId:(.*?),.*?}', re.S)
        items = re.findall(pattern, source_data)
        contents = []
        for item in items:
            contents.append([item[0], item[1], item[2], item[3], item[4], item[5], item[6]])
        return contents

    def get_model_info(self, model_id):
        info_url = 'https://mm.taobao.com/self/info/model_info_show.htm?user_id=' + str(model_id)
        response = requests.get(info_url).text
        model_info = []
        pattern = re.compile('<ul class="mm-p-info-cell clearfix">.*?<span>(.*?)</span>.*?<span>(.*?)'
                             '</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)'
                             '</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<p>(.*?)\D+</p>.*?'
                             '<p>(.*?)\D+</p>.*?<p>(.*?)</p>.*?<p>(.*?)</p>.*?<p>(.*?)\D</p>', re.S)
        items = re.findall(pattern, response)
        for item in items:
            birthday = item[1].strip()
            birthday = self.remove_space(birthday)
            education = item[5].strip()
            education = self.remove_space(education)
            model_info.append([item[0], birthday, item[2], item[3], item[4], education, item[6],
                               item[7], item[8], item[9], item[10], item[11]])
        return model_info

    @staticmethod
    def get_album_list(model_id):
        # Get page number of all albums, after this, crawl all the pages and find the link and name of all these albums
        first_album_list_url = 'https://mm.taobao.com/self/album/open_album_list.htm?user_id=' + str(model_id)
        find_total_page = requests.get(first_album_list_url).text
        page_no_pattern = re.compile('<input name="totalPage.*?value="(.*?)" type="hidden" />', re.S)
        total_page = re.findall(page_no_pattern, find_total_page)
        # print total_page[0], type(total_page[0])
        albums = []
        for i in xrange(1, int(total_page[0])+1):
            album_list_url = first_album_list_url + '&page=' + str(i)
            # print album_list_url  # Just for testing
            album_link_page = requests.get(album_list_url).text
            pattern = re.compile('<h4>.*?album_id=(.*?)\D.*?>(.*?)</a></h4>.*?mm-pic-number">\((.*?)\D', re.S)
            # album_link_pattern = re.compile('<h4>.*?&album_id=(.*?)&album_flag.*?target="_blank">(.*?)'
            #                                 '</a></h4>.*?mm-pic-number">\((.*?)张\)</span>', re.S)
            album_list = re.findall(pattern, album_link_page)
            for item in album_list:
                album_name = item[1].strip()  # Something wrong here (fixed by strip()).
                # item[0]=album id, item[1]=album name
                # item[2]=how many pictures in this album
                albums.append([item[0], album_name, item[2]])
        # print albums  # Just for testing
        return albums

    def download_all_album(self, model_id, model_name):
        self.make_folder('mm.taobao' + '/' + model_name)
        album_info = self.get_album_list(model_id)
        for album in album_info:
            album_name = self.remove_dot(album[1])
            print 'Album ' + album_name + ' has ' + str(album[2]) + ' pictures'
            self.make_folder('mm.taobao' + '/' + model_name + '/' + album_name)
            print 'Downloading album ' + album_name
            image_list = self.get_img_link(model_id, album[0])
            for image_url in image_list:
                self.save_img(image_url, 'mm.taobao' + '/' + model_name + '/' + album_name)

    def single_model_all_albums(self, model_id):
        # Download a single model's albums by her id
        model_info = self.get_model_info(model_id)
        model_name = model_info[0][0]
        self.download_all_album(model_id, model_name)

    def single_album_all_pictures(self, model_id, album_id):
        # Download a single album by model_id and album_id
        print 'Getting model name and album info...'
        albums = self.get_album_list(model_id)
        model_info = self.get_model_info(model_id)
        model_name = model_info[0][0]
        self.make_folder('mm.taobao' + '/' + model_name)
        for album in albums:
            # print album
            if album_id == album[0]:
                album_name = self.remove_dot(album[1])
                print 'Album ' + album_name + ' has ' + str(album[2]) + ' pictures'
                self.make_folder('mm.taobao' + '/' + model_name + '/' + album_name)
                print 'Downloading album ' + album_name
                image_list = self.get_img_link(model_id, album[0])
                for image_url in image_list:
                    self.save_img(image_url, 'mm.taobao' + '/' + model_name + '/' + album_name)

    @staticmethod
    def get_img_link(model_id, album_id):
        image_url = []
        first_album_url = 'https://mm.taobao.com/album/json/get_photo_list_tile_data.htm?user_id='\
                          + str(model_id) + '&album_id=' + str(album_id)
        response = requests.get(first_album_url).text
        page_no_pattern = re.compile('<input name="totalPage.*?value="(.*?)" type="hidden" />', re.S)
        total_page = re.findall(page_no_pattern, response)
        print 'Collecting all picture links in this album...'
        for i in xrange(1, int(total_page[0])+1):
            album_url = first_album_url + '&page=' + str(i)
            response = requests.get(album_url).text
            pattern = re.compile('<img src="(.*?)" class.*?', re.S)
            image_urls = re.findall(pattern, response)
            for item in image_urls:
                image_url.append('http:' + item)
        return image_url

    @staticmethod
    def save_img(thread_name, image_url, folder_name):
        image_name = image_url.split('/').pop()
        image_location = folder_name + '/' + image_name
        if not os.path.isfile(image_location):
            print thread_name + ': Saving picture ' + image_name
            image_data = requests.get(image_url)
            f = open(image_location, 'wb')
            f.write(image_data.content)
            f.close()
        else:
            print image_name + ' already exists, skip...'

    @staticmethod
    def make_folder(folder_name):  # folder_name is model name or album name
        if not os.path.exists(folder_name):
            print 'Making folder "' + folder_name + '"'
            os.mkdir(folder_name)
        else:
            print 'Folder "' + folder_name + '" already exists, skip...'

    @staticmethod
    def remove_double_quotation_marks(source_data):
        # Some small 'formatted' of the page source.
        pattern = re.compile('\"')
        source_data = re.sub(pattern, '', source_data)
        return source_data

    @staticmethod
    def remove_space(source_data):
        pattern = re.compile('&nbsp;')
        source_data = re.sub(pattern, '', source_data)
        return source_data

    @staticmethod
    def remove_dot(source_data):
        pattern = re.compile('\.')
        source_data = re.sub(pattern, '', source_data)
        source_data = re.sub('\/', '-', source_data)
        return source_data

    def save_info(self, start_page, end_page):
        # Something like the main function.
        self.make_folder('mm.taobao')
        csv_file = file('mm.taobao/model_info.csv', 'wb')
        writer = csv.writer(csv_file, dialect='excel')
        writer.writerow(['昵称', '生日', '所在城市', '职业', '血型', '学校/专业', '风格',
                         '身高(cm)', '体重(kg)', '三围', '罩杯', '鞋码(码)', '粉丝数', '点赞数', 'ID'])
        for page_index in xrange(start_page, end_page+1):
            contents = self.get_contents(page_index)
            print '='*20 + 'PAGE ' + str(page_index) + '='*20
            for item in contents:
                # Found the popular model and skip these that is not so popular.
                if int(item[4]) > 1000 or int(item[5]) > 500:
                    print 'Found a popular model, her name is ' + item[3] + ', she has ' + str(item[4]) + \
                          ' fans and her total favor number is ' + str(item[5])
                    print 'Writing ' + item[3] + "'s info..."
                    model_info = self.get_model_info(str(item[6]))
                    writer.writerow([model_info[0][0], model_info[0][1], model_info[0][2], model_info[0][3],
                                    model_info[0][4], model_info[0][5], model_info[0][6], model_info[0][7],
                                    model_info[0][8], model_info[0][9], model_info[0][10], model_info[0][11],
                                    item[4], item[5], item[6]])
                else:
                    print 'Found a model, her name is ' + item[3] + ', but she is not very popular, skip...'
        csv_file.close()

    def download_picture(self, start_page, end_page):
        self.make_folder('mm.taobao')
        for page_index in xrange(start_page, end_page+1):
            contents = self.get_contents(page_index)
            for item in contents:
                # Found the popular model and skip these that is not so popular.
                if int(item[4]) > 1000 or int(item[5]) > 500:
                    print 'Found a popular model, her name is ' + item[3] + ', she has ' + str(item[4]) + \
                          ' fans and her total favor number is ' + str(item[5])
                    model_name = self.remove_dot(item[3])
                    # self.make_folder('mm.taobao' + '/' + model_name)
                    self.download_all_album(item[6], model_name)
                else:
                    print 'Found a model, her name is ' + item[3] + ', but she is not very popular, skip...'

# demo = TaobaoMM()
# demo.save_info(1, 2)
# Download a single model's albums by her id and name
# demo.single_model_all_albums('141234233')
# demo.download_picture(1, 1)
# demo.single_album_all_pictures('141234233', '10001066316')
