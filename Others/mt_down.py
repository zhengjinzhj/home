#!/usr/bin/env python
# -*- coding: utf-8 -*-

from queue import Queue
from tools import *
from club import *

queue = Queue()


def create_workers():
    for _ in range(4):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        url = queue.get()
        mt_downloader(url)
        # st_downloader(url, rename='with_subdir')
        queue.task_done()


def create_jobs():
    for link in get_pic_urls(get_page_urls(get_info())):
        queue.put(link)
    queue.join()


make_folder('D:\Download', '108j.club')
create_workers()
create_jobs()
