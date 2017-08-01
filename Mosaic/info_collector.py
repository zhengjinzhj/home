# -*- coding:utf-8 -*-

from tools import *


class AV9898(object):
    base_url = 'http://www.heydouga.com/listpages/provider_4030_'
    base_cover_url = 'http://image01.heydouga.com/contents/4030/'
    folder_location = 'D:\Download\\1005051773261093\\NoMosaic'
    folder_name = 'av9898'

    def __init__(self):
        os.chdir(AV9898.folder_location)
        make_folder(AV9898.folder_name)
        os.chdir(AV9898.folder_location + '\\' + AV9898.folder_name)

    @staticmethod
    def get_latest_video():
        first_url = AV9898.base_url + '1.html'
        print('Now getting the latest video from %s' % first_url)
        soup = get_page_source(first_url)
        latest_video_item = soup.find('div', class_='movie-image').find('a')
        latest_video = latest_video_item['href'].split('/')[-2]
        print('The latest_video No. is %s' % latest_video)
        return int(latest_video)

    @staticmethod
    def get_cover_links():
        # latest_video = AV9898.get_latest_video()
        cover_urls = []
        for video_no in range(1952, 2018):
            if video_no < 10:
                video_no = '00' + str(video_no)
            elif video_no < 100:
                video_no = '0' + str(video_no)
            else:
                video_no = str(video_no)
            cover_url = AV9898.base_cover_url + video_no + '/player_thumb.jpg'
            cover_urls.append(cover_url)
        return cover_urls

    @staticmethod
    def get_file_name(cover_url):
        return cover_url.split('/')[-2] + '.jpg'

    @staticmethod
    def download_img(thread_name, cover_url):
        file_name = AV9898.get_file_name(cover_url)
        save_img(thread_name, cover_url, file_name)


# class Musume(AV9898):
# # http://www.10musume.com/moviepages/011417_01/images/str.jpg
# # http://www.10musume.com/listpages/1_211.html
# # 遠山雪菜, 岡田優子, さくら林檎 田中美佐 間柴京花 白川メイナ, 須藤望(聲音很誘人), 島崎美優, 佐々木梓, 秋吉みなみ, 藤井彩香
#
#     def __init__(self):
#         self.main_url = 'http://www.tokyo-hot.com/product/'
#         self.base_url = 'http://my.cdn.tokyo-hot.com/media/'
#         self.parameter = {'filter': '撮りおろし徹底陵辱ビデオ', 'type': 'genre'}
#
#     def get_total_page(self):
#         first_url = self.main_url
#         data = requests.get(first_url, params=self.parameter, proxies=proxy)
#         content = data.text
#         total_page = re.findall('<p class="naviend"><a href="\?page=(.*?)&amp', content)
#         return int(total_page[0])
#
#     def get_video_id(self):
#         total_page = self.get_total_page()
#         all_video_id = []
#         for page_no in range(1, total_page+1):
#             if page_no == 1:
#                 url = self.main_url
#             else:
#                 url = self.main_url + '?page=' +str(page_no)
#             data = requests.get(url, params=self.parameter, proxies=proxy)
#             soup = BeautifulSoup(data.text, 'html.parser')
#             for item in soup.find('ul', class_='slider').find_all('a'):
#                 video_page = item['href']
#                 video_id = video_page.split('/')[-2]
#                 all_video_id.append(video_id)
#         return all_video_id


class DMM(object):
    input_url = 'http://www.dmm.co.jp/digital/videoa/-/list/=/article=keyword/id=4005/' \
                'sort=bookmark_desc/trans_type=dl6/page=2'

    @staticmethod
    def get_cover_url():
        soup = get_page_source(DMM.input_url)
        # print soup.prettify()
        for item in soup.find('div', class_='d-item').find_all('img'):
            small_cover = item['src']
            cover = small_cover.replace('pt', 'pl')
            print(cover)


# demo = AV9898()
# demo.save_link_to_file()

# demo = TokyoHot()
# demo.get_total_page()
# demo.get_video_id()

# demo = DMM()
# demo.get_cover_url()



