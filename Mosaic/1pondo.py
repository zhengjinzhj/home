# -*- coding:utf-8 -*-

import csv
import requests
import json
from bs4 import BeautifulSoup

ssr_proxy = {'http': '127.0.0.1:1080', 'https': '127.0.0.1:1080'}
base_url_1pondo = 'http://www.1pondo.tv/dyn/ren/movie_lists/list_newest_'
csv_title_1pondo = ['Movie ID', 'Release Date', 'Title', 'Actress', 'Description',
                    'Series', 'Year', 'Tags', 'Actor ID', 'Cover']
base_url_carib = 'http://www.caribbeancom.com/listpages/all'
csv_title_carib = ['Movie ID', 'Release Date', 'Title', 'Actress', 'Cover']
base_url_th = 'http://www.tokyo-hot.com/product/?page='
csv_title_th = ['Movie ID', 'Series No', 'Title', 'Actress', 'Cover']
# http://smovie.1pondo.tv/sample/movies/092916_394/1080p.mp4
# http://smovie.caribbeancom.com/sample/movies/110616-297/1080p.mp4
# http://my.cdn.tokyo-hot.com/media/samples/6081.mp4
# http://sample.heyzo.com/contents/3000/1313/heyzo_hd_1313_sample.mp4
# http://sample.heyzo.com/contents/3000/0001/sample.mp4


# http://stackoverflow.com/questions/28165639/
# http://stackoverflow.com/questions/20994352
# Pickle files are binary data files, so you always have to open the file with the 'rb' mode when loading.

# json.loads take a string as input and returns a dictionary as output.
# json.dumps take a dictionary as input and returns a string as output.
# json.load is for file, while json.loads is for string


# for 1pondo.tv, 51 for ONE page, 101 for TWO page
def get_contents(base_url, page_no):
    contents = []
    if 'pond' in base_url:
        for page in range(0, page_no, 50):
            url = base_url + str(page) + '.json'
            print('*'*20 + 'Now crawling ' + str(page) + '.json' + '*'*20)
            response = requests.get(url, proxies=ssr_proxy).text
            temp = json.loads(response)
            wanted_content = []
            for content in temp['Rows']:
                content.setdefault('Series', '')
                description = content['Desc'].replace('\r', '').replace('\n', '')
                tags = ','.join(content['UCNAME'])
                wanted_content = [content['MovieID'], content['Release'], content['Title'], content['Actor'],
                                  description, content['Series'], content['Year'], tags,
                                  content['ActorID'][0], content['ThumbHigh']]
            contents.append(wanted_content)
    elif 'carib' in base_url:
        for page in range(1, page_no+1):
            url = base_url + str(page_no) + '.htm'
            print('*'*20 + 'Now crawling page ' + str(page) + '*'*20)
            response = requests.get(url, proxies=ssr_proxy).text
            soup = BeautifulSoup(response, 'html.parser')
            wanted_content = []
            for item in soup.select('div[itemtype="http://schema.org/VideoObject"]'):
                # Or soup.find_all(itemtype='http://schema.org/VideoObject')
                release_date = item.find(class_='movie-date').string.strip()
                movie_id = item.a['href'].split('/')[2]
                # item.a['href] == item.a.get('href)
                alt = item.img.get('alt')
                thumbnail = item.img.get('src').replace('256x144', '')
                title = item.img.get('title')
                actress = alt.replace(title, '').strip()
                wanted_content = [movie_id, release_date, title, actress, thumbnail]
            contents.append(wanted_content)
    elif 'tokyo-hot' in base_url:
        for page in range(1, page_no+1):
            url = base_url + str(page_no)
            parameter = {'filter': '撮りおろし徹底陵辱ビデオ', 'type': 'genre'}
            print('*'*20 + 'Now crawling page ' + str(page) + '*'*20)
            response = requests.get(url, proxies=ssr_proxy, params=parameter).text
            soup = BeautifulSoup(response, 'html.parser')
            wanted_content = []
            for item in soup.find_all(class_='detail'):
                title = item.find(class_='title').string.strip()
                movie_id = item.a.get('href').split('/')[2]
                series_no = item.img.get('alt')
                thumbnail = item.img.get('src').replace('220x124', '820x462')
                actress = item.find(class_='actor').string.strip()[:-14]
                wanted_content = [movie_id, series_no, title, actress, thumbnail]
            contents.append(wanted_content)
    return contents


def write_csv_file(filename, title, contents):
    with open(filename, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, dialect='excel')
        writer.writerow(title)
        for content in contents:
            writer.writerow(content)
    csv_file.close()
