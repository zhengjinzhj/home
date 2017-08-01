# -*- coding:utf-8 -*-

import threading
from queue import Queue
from info_collector import AV9898

queue = Queue()
AV9898()


def create_workers():
    for _ in range(8):
        worker = threading.Thread(target=work)
        worker.daemon = True
        worker.start()


def work():
    while True:
        cover_url = queue.get()
        AV9898.download_img(threading.current_thread().name, cover_url)
        queue.task_done()


def create_jobs():
    for cover_url in AV9898.get_cover_links():
        queue.put(cover_url)
    queue.join()

create_workers()
create_jobs()

