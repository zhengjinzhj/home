# -*- coding:utf-8 -*-

import csv
import requests
import json

ssr_proxy = {'http': '127.0.0.1:1080', 'https': '127.0.0.1:1080'}
base_url_1pondo = 'http://www.1pondo.tv/dyn/ren/movie_lists/list_newest_'
csv_title_1pondo = ['Movie ID', 'Title', 'Actor', 'Description', 'Release',
                    'Series', 'Year', 'Tags', 'Cover', 'Actor ID']
base_url_carib = 'http://www.caribbeancom.com/listpages/all'
csv_title_carib = ['Movie ID', 'Release Date', 'Title', 'Actress', 'Cover']
# http://smovie.1pondo.tv/sample/movies/092916_394/1080p.mp4
# http://smovie.caribbeancom.com/sample/movies/110616-297/1080p.mp4


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
            response = requests.get(url, proxies=ssr_proxy)
            temp = json.loads(response.text)
            wanted_content = []
            for content in temp['Rows']:
                content.setdefault('Series', '')
                description = content['Desc'].replace('\r', '').replace('\n', '')
                tags = ','.join(content['UCNAME'])
                wanted_content = [content['MovieID'], content['Title'], content['Actor'], description,
                                  content['Release'], content['Series'], content['Year'], tags,
                                  content['ThumbHigh'], content['ActorID'][0]]
            contents.append(wanted_content)
    else:
        for page in range(1, page_no+1):
            url = base_url + str(page_no) + '.htm'
            print('*'*20 + 'Now crawling page ' + str(page) + '*'*20)
            response = requests.get(url, proxies=ssr_proxy)
    return contents


def write_csv_file(filename, title, contents):
    with open(filename, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, dialect='excel')
        writer.writerow(title)
        for content in contents:
            writer.writerow(content)
    csv_file.close()
