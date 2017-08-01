# -*- coding:utf-8 -*-

# import requests
from bs4 import BeautifulSoup
import os
import time
from proxy import request
from queue import MongoQueue
import threading
import multiprocessing


class MeiZi(object):

    def __init__(self):
        self.crawl_queue = MongoQueue('MeiZi', 'crawl_queue')
        self.img_queue = MongoQueue('MeiZi', 'img_queue')
        self.SLEEP_TIME = 1

    @staticmethod
    # 公共方法，抓取页面并返回通过BeautifulSoup解析后的页面源码
    def get_page_source(url):
        html = request.get(url, 3)
        soup = BeautifulSoup(html.text, 'html.parser')
        return soup

    # 从BeautifulSoup解析后的页面源码中解析出相册即其地址并返回2阶数组（此处仅解析最近一个月的相册）
    def gather_albums(self, url):
        soup = self.get_page_source(url)
        # albums = []
        for album in soup.find('p', class_='url').find_all('a'):
            # one_album = []
            link = album['href']
            album_name = album.string.strip()
            self.crawl_queue.push(link, album_name)
            # one_album.append(link)
            # one_album.append(album_name)
            # albums.append(one_album)
        # return albums

    # 通过相册第一页获取相册的大小（共多少页）
    def get_album_size(self, album_url):
        soup = self.get_page_source(album_url)
        temp = soup.find('div', class_='pagenavi').find_all('span')
        total_page = temp[-2].string
        return int(total_page)

    # 从相册的每一页中获取图片的原始链接（每页一张图片）
    def get_picture_link(self, page_link):
        soup = self.get_page_source(page_link)
        link = soup.find('img')
        return link['src']

    @staticmethod
    # 公共方法，创建文件夹
    def make_folder(folder_name):
        if not os.path.exists(folder_name):
            print 'Creating folder: %s' % folder_name
            os.mkdir(folder_name)
        else:
            print 'Folder already exists, skip...'

    @staticmethod
    # 公共方法，下载图片
    def save_img(picture_url):
        data = request.get(picture_url, 3)
        file_name = picture_url.split('/')[-1]
        print 'Downloading picture: %s' % file_name
        f = open(file_name, 'wb')
        f.write(data.content)
        f.close()

    # 通过调用这种方法，下载一个相册（一套图）
    # def download_one_album(self, link, album_name):
    def download_one_album(self):
        while True:
            try:
                link = self.crawl_queue.pop()
                print link
            except KeyError:
                print '队列中没有数据'
                break
            else:
                img_urls = []
                path = 'D:\Download\mzitu'
                os.chdir(path)
                album_name = self.crawl_queue.pop_title(link)
                self.make_folder(album_name)
                os.chdir(path + '\\' + album_name)
                total_page = self.get_album_size(link)
                print 'There are %d pictures in this album.' % total_page
                # page_num = 0  # 添加一个计数器判断相册是否下载完毕
                for page in xrange(1, total_page+1):
                    # page_num += 1  # 当page_num=total_page时，就是下载相册中最后一张图片的时候
                    page_link = link + '/' + str(page)
                    picture_url = self.get_picture_link(page_link)
                    img_urls.append(picture_url)
                    self.save_img(picture_url)
                    # if page_num == total_page:
                    #     self.save_img(picture_url)
                    #     post = {
                    #         '相册名称': album_name,
                    #         '相册地址': link,
                    #         '图片地址': picture_url,
                    #         '获取时间': time.ctime()
                    #     }
                    #     self.beauty_collect.save(post)
                    #     print '插入数据库成功'
                    # else:
                    #     self.save_img(picture_url)
                self.crawl_queue.complete(link)  # 设置为完成状态
                self.img_queue.push_img_url(album_name, img_urls)
                print '插入数据库成功'

    def main(self):  # will NOT be used with multi threads and processes
        ts = time.time()
        os.chdir('D:\Download')
        self.make_folder('mzitu')
        # main_url = 'http://www.mzitu.com/all'
        # for album in self.gather_albums(main_url):
        #     if self.beauty_collect.find_one({'相册地址': album[0]}):
        #         print 'This Album already downloaded, skip...'
        #     else:
        #         self.download_one_album(album[0], album[1])
        # First time: 1036 files in 20 folders, 113MB in 207.34499979 seconds. (No proxy, no user agent)
        # Second time: 1148 files in 22 folders, 125MB in 250.858999968 seconds. (With proxy and user agent)
        print 'Take %s seconds in total.' % (time.time() - ts)

    def threads_crawler(self, max_threads=10):
        self.download_one_album()
        threads = []
        while threads or self.crawl_queue:
            # 这里crawl_queue用上了，就是__bool__函数的作用，为真则代表MongoDB队列里面还有数据
            # threads或者crawl_queue为真都代表下载还没有完成，程序都会继续执行
            for thread in threads:
                if not thread.is_alive():  # 判断是否为空，不为空则在队列中删除
                    threads.remove(thread)
            while len(threads) < max_threads or self.crawl_queue.peek():  # 线程池中的线程少于a或b时
                thread = threading.Thread(target=self.download_one_album)  # 创建线程
                thread.setDaemon(True)  # 设置守护线程
                thread.start()  # 启动线程
                threads.append(thread)  # 添加线程到队列
            time.sleep(self.SLEEP_TIME)

    def process_crawler(self):
        process = []
        num_cpu = multiprocessing.cpu_count()
        print '将启动个%d进程' % num_cpu
        for _ in range(num_cpu):
            p = multiprocessing.Process(target=self.threads_crawler)
            p.start()
            process.append(p)
        for p in process:
            p.join()  # 等待进场队列里的进场结束


demo = MeiZi()
# demo.main()
demo.process_crawler()




























