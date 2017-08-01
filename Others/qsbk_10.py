#!/usr/bin/python
# filename: qsbk_10.py

# -*- coding: utf-8 -*-

import urllib2
import re


class QSBK:
    def __init__(self):
        self.pageindex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}
        self.storage = []
        self.enable = False

    def getpage(self, pageindex):  # get one page
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageindex) + '/?s=4880776'
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pagecode = response.read().decode('utf-8')
            pattern = re.compile('<div.*?author.*?>.*?<img.*?>.*?<h2>(.*?)</h2>.*?<div.*?' +
                                 'content">(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>', re.S)

            items = re.findall(pattern, pagecode)

            for item in items:
                haveimg = re.search("img", item[2])
                if not haveimg:
                    replacebr = re.compile('<br/>')
                    text = re.sub(replacebr, "\n", item[1])
                    self.storage.append([item[0], item[3], text])

        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
            return None

    def start(self):
        print "reading...,print 'Enter' to read one story, pirnt 'q' to quit"
        self.enable = True

        while self.enable:
            self.getpage(self.pageindex)
            for i in range(len(self.storage)):
                input = raw_input()
                if input == "q":
                    self.enable = False
                    return
                print "page:%d, number:%d\nauthor: %s\nprise : %s\n%s" % (
                self.pageindex, i, self.storage[i][0].strip(), self.storage[i][1].strip(), self.storage[i][2].strip())

            self.pageindex += 1
            self.storage = []  # clear list


spider = QSBK()
spider.start()
