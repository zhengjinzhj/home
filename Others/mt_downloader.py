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

import threading
from queue import Queue
from tools import *
from Others.club import *
import datetime

# download_url = sys.argv[1]  # 传入的命令行参数，要下载文件的url
# download_url = 'http://patch2.51mag.com/2017/ALI213-Halo-Wars-2-V1.4.1936.2-Trainer%205MrAntiFun.rar'


def handler(start, end, url, filename):
    headers = {
        'Range': 'bytes=%d-%d' % (start, end)
    }
    r = requests.get(url, headers=headers, stream=True)

    # 写入文件对应的位置
    with open(filename, 'r+b') as fp:
        fp.seek(start)
        fp.tell()
        fp.write(r.content)


def download_file(url, num_thread=2):
    parts = url.split('/')
    file_name = parts[-2] + '_' + parts[-1]
    if not os.path.isfile(file_name):
        print('%s> Downloading file: %s' % (datetime.datetime.now(), file_name))
        r = requests.head(url)
        try:
            # Content-Length获得文件主体的大小，当http服务器使用Connection:keep-alive时，不支持Content-Length
            file_size = int(r.headers['content-length'])
        except:
            print('Please check the url, or file %s does not support multi threading download' % file_name)
            return

        # 创建一个和要下载文件一样大小的文件
        fp = open(file_name, 'wb')
        fp.truncate(file_size)
        fp.close()

        # 启用多线程写文件
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

        # 等待所有线程下载完毕
        # main_thread = threading.current_thread()
        # threading.enumerate()返回一个包含正在运行的线程的list。正在运行指线程启动后、结束前，不包括启动前和终止后的线程。
        # for t in threading.enumerate():
        #     if t is main_thread:
        #         continue
        #     t.join()
        print('%s> %s downloading complete!' % (datetime.datetime.now(), file_name))
    else:
        print('%s> %s already exists, skip...' % (datetime.datetime.now(), file_name))

# if __name__ == '__main__':
#     start_time = datetime.datetime.now().replace(microsecond=0)
#     download_file(download_url)
#     end_time = datetime.datetime.now().replace(microsecond=0)
#     print('用时： ', end='')
#     print(end_time-start_time)

queue = Queue()


def create_workers():
    for _ in range(4):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        url = queue.get()
        download_file(url)
        # save_file(url, file_name='with_subdir')
        queue.task_done()


def create_jobs():
    for link in get_pic_urls(get_page_urls(get_info())):
        queue.put(link)
    queue.join()


make_folder('D:\\Download\\1005051773261093', '108j.club')
create_workers()
create_jobs()
