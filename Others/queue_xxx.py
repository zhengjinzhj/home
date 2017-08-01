# -*- coding:utf-8 -*-

from datetime import datetime, timedelta
from pymongo import MongoClient, errors


class MongoQueue(object):

    OUTSTANDING = 1  # default status
    PROCESSING = 2  # downloading
    COMPLETE = 3  # download complete

    def __init__(self, db, collection, timeout=300):  # initialize the connection of MongoDB
        self.client = MongoClient()  # 与MongoDB建立连接（默认连接本地的MongoDB数据库）
        self.db = self.client[db]  # 选择一个数据库
        self.collection = self.db[collection]  # 在选择的数据库中选择一个集合（表）
        # MongoDB不需要先创建数据库和集合（表），存在则直接写入，不存在则先创建需要的数据库和集合再写入数据。
        self.timeout = timeout

    def __bool__(self):
        # 如果下面的表达式为真，则整个类为真。
        # $ne的意思是“不匹配”
        record = self.collection.find_one(
            {'status': {'$ne': self.COMPLETE}}
        )
        return True if record else False

    def push(self, url, title):  # 添加新的URL进队列
        try:
            self.collection.insert({'_id': url, 'status': self.OUTSTANDING, '主题': title})
            print url, '插入队列成功'
        except errors.DuplicateKeyError:
            print url, '已经存在于队列中了'
            pass

    def push_img_url(self, title, url):
        try:
            self.collection.insert({'_id': title, 'status': self.OUTSTANDING, 'url': url})
            print '图片地址插入成功'
        except errors.DuplicateKeyError:
            print '地址已经存在了'
            pass

    def pop(self):
        """
        查询队列中所有状态为OUTSTANDING的值、更改状态（query后面是查询，update后面是更新），
        并返回_id（即URL）。如果没有OUTSTANDING的值，则调用repair()函数重置所有超时的状态为OUTSTANDING。
        $set为设置
        """
        record = self.collection.find_and_modify(
            query={'status': self.OUTSTANDING},
            update={'$set': {'status': self.PROCESSING, 'timestamp': datetime.now()}}
        )
        if record:
            return record['_id']
        else:
            self.repair()
            raise KeyError

    def repair(self):
        # 重置状态。$ls是比较
        record = self.collection.find_and_modify(
            query={'timestamp': {'$lt': datetime.now() - timedelta(seconds=self.timeout)},
                   'status': {'$ne': self.COMPLETE}
                   },
            update={'$set': {'status': self.OUTSTANDING}}
        )
        if record:
            print '重置URL状态', record['_id']

    def pop_title(self, url):
        record = self.collection.find_one({'_id': url})
        return record['主题']

    def peek(self):
        # 取出状态为OUTSTANDING的文档（数据记录行）并返回_id(URL)
        record = self.collection.find_one({'status': self.OUTSTANDING})
        if record:
            return record['_id']

    def complete(self, url):
        # 更新已完成的URL为完成状态
        self.collection.update({'_id': url}, {'$set': {'status': self.COMPLETE}})

    def clear(self):
        # 删表！只有第一次才调用
        self.collection.drop()











































