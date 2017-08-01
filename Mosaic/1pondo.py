# -*- coding:utf-8 -*-

import csv
import requests
import json

proxy = {'http': '127.0.0.1:1080'}
main_url = 'http://www.1pondo.tv/dyn/ren/movie_lists/list_newest_'
# http://smovie.1pondo.tv/sample/movies/092916_394/1080p.mp4


# http://stackoverflow.com/questions/28165639/
# Pickle files are binary data files, so you always have to open the file with the 'rb' mode when loading.

# json.loads take a string as input and returns a dictionary as output.
# json.dumps take a dictionary as input and returns a string as output.
# json.load is for file, while json.loads is for string

with open('list_newest_0.json', 'rb') as json_file:
    temp = json.load(json_file)
    # pprint(temp)


# http://stackoverflow.com/questions/20994352
with open('test.csv', 'w', encoding='utf-8', newline='') as csv_file:
    writer = csv.writer(csv_file, dialect='excel')
    writer.writerow(['Movie ID', 'Title', 'Actor', 'Description', 'Release',
                     'Series', 'Year', 'Tags', 'Cover', 'Actor ID'])
    for page in range(0, 151, 50):  # 2017-03-19
        url = main_url + str(page) + '.json'
        print('Now crawling ' + str(page) + '.json')
        request = requests.get(url, proxies=proxy)
        temp = json.loads(request.text)
        for content in temp['Rows']:
            content.setdefault('Series', '')
            description = content['Desc'].replace('\r', '').replace('\n', '')
            tags = ','.join(content['UCNAME'])
            wanted_content = [content['MovieID'], content['Title'], content['Actor'], description,
                              content['Release'], content['Series'], content['Year'], tags,
                              content['ThumbHigh'], content['ActorID'][0]]
            writer.writerow(wanted_content)
csv_file.close()
