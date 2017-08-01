#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from Queue import Queue
from taobaomm import TaobaoMM

model_id = '2926468580'
album_id = '10001044155'
queue = Queue()


def create_jobs():
    for img_link in TaobaoMM.get_img_link(model_id, album_id):
        queue.put(img_link)
    queue.join()


def get_albums():
    for album in TaobaoMM.get_album_list(model_id):
        album_id = album[0]
        album_name = album[1]
        album_page = album[2]
        print 'There are %s pictures in %s: %s' % (album_page, album_name, album_id)
        TaobaoMM.make_folder(album_name)
        create_jobs(album_id, album_name)


def create_workers():
    for _ in xrange(4):
        worker = threading.Thread(target=work)
        worker.daemon = True
        worker.start()


def work():
    while True:
        image_url = queue.get()
        # album_name = queue.get()[1]
        TaobaoMM.save_img(threading.current_thread().name, image_url, album_id)
        queue.task_done()

TaobaoMM.make_folder(album_id)
create_workers()
create_jobs()
