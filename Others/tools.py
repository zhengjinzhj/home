#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
http://blog.topspeedsnail.com/archives/8462
multi threading downloader

基本步骤：
1. 把要下载的文件平均分成几块
2. 每个线程分别下载对应的块
3. 把各块写入到文件中相应的位置

"""

import os
import requests
import threading
import time

# download_url = sys.argv[1]  # 传入的命令行参数，要下载文件的url
download_url = 'http://patch2.51mag.com/2017/ALI213-Halo-Wars-2-V1.4.1936.2-Trainer%205MrAntiFun.rar'


def handler(start, end, url, filename):
    # only for mt_downloader using
    headers = {
        'Range': 'bytes=%d-%d' % (start, end)
    }
    r = requests.get(url, headers=headers, stream=True)

    # 写入文件对应的位置
    with open(filename, 'r+b') as fp:
        fp.seek(start)
        # fp.tell()  # current file position
        fp.write(r.content)


def mt_downloader(url, rename='', num_thread=2):
    # multi threading downloader, 2 threads by default
    # Rename the saving file or not
    if rename == 'with_subdir':
        parts = url.split('/')
        file_name = parts[-2] + '_' + parts[-1]
    elif rename == 'only_subdir':
        name = url.split('/')[-2]
        extension = url.split('.')[-1]
        file_name = name + '.' + extension
    else:
        file_name = url.split('/').pop()

    if not os.path.isfile(file_name):
        print('%s> Downloading file: %s' % (time.strftime('%H:%M:%S'), file_name))
        r = requests.head(url)
        try:
            # Content-Length获得文件主体的大小，当http服务器使用Connection:keep-alive时，不支持Content-Length
            file_size = int(r.headers['content-length'])
            if r.status_code != 200:
                print('%s: Please check the url!' % file_name)
        except KeyError:
            print('File %s does not support multi threading download' % file_name)
            return

        # # 创建一个和要下载文件一样大小的文件, 非必须
        # fp = open(file_name, 'wb')
        # fp.truncate(file_size)
        # fp.close()

        # 启用多线程写文件
        thread_list = list([])
        part = file_size // num_thread
        for i in range(num_thread):
            start = part * i
            if i == num_thread - 1:
                end = file_size
            else:
                end = start + part

            t = threading.Thread(target=handler, kwargs={'start': start, 'end': end, 'url': url, 'filename': file_name})
            t.setDaemon(True)
            t.start()
            thread_list.append(t)

        # 等待所有线程下载完毕
        # main_thread = threading.current_thread()
        # threading.enumerate()返回一个包含正在运行的线程的list。正在运行指线程启动后、结束前，不包括启动前和终止后的线程。
        # for t in threading.enumerate():
        #     if t is main_thread:
        #         continue
        #     t.join()
        for t in thread_list:
            t.join()
        print('%s> %s downloading complete!' % (time.strftime('%H:%M:%S'), file_name))
    else:
        print('%s> %s already exists, skip...' % (time.strftime('%H:%M:%S'), file_name))

if __name__ == '__main__':
    # start_time = datetime.datetime.now().replace(microsecond=0)
    mt_downloader(download_url)
    # end_time = datetime.datetime.now().replace(microsecond=0)
    print('用时： ', end='')
    # print(end_time-start_time)


def st_downloader(url, rename=''):
    # single threading downloader
    # If file name is not provided, use its name original name in the url
    if rename == 'with_subdir':
        parts = url.split('/')
        file_name = parts[-2] + '_' + parts[-1]
    elif rename == 'subdir':
        name = url.split('/')[-2]
        extension = url.split('.')[-1]
        file_name = name + '.' + extension
    else:
        file_name = url.split('/').pop()
    if not os.path.isfile(file_name):
        print('Downloading %s' % file_name)
        response = requests.get(url)
        file = open(file_name, 'wb')
        file.write(response.content)
        file.close()
    else:
        print('%s already exists, skip...' % file_name)


def make_folder(location, folder):
    # make folder and switch to the directory
    directory = os.path.join(location, folder.strip())
    if not os.path.exists(directory):
        print('Creating directory: %s' % directory)
        os.makedirs(directory)
        os.chdir(directory)  # Switch to the directory
        # print(os.getcwd())  # Print current directory
    else:
        print('%s already exists, skip...' % directory)
        os.chdir(directory)


# make_folder('D:\download\游戏', 'cs_go')
# st_downloader('http://cdn.steamstatic.com.8686c.com/steam/apps/81958/movie480.webm')
