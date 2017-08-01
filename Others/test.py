#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import http.client
#
# url = '10.82.12.26:9090'
# param = '/login'
#
# conn = http.client.HTTPConnection(url)
# conn.request('POST', param)
# response = conn.getresponse()
# status = response.status
# resp = response.read()
#
# print(type(status))
# print(resp.decode('utf-8'))

# ========================
# width = int(input('Please enter the width: '))
# price_width = 10
# item_width = width - price_width
#
# header_format = '%-*s%-*s'
# content_format = '%-*s%-*.2f'
#
# print('=' * width)
#
# print(header_format % (item_width, 'Item', price_width, 'Price'))
#
# print('-' * width)
#
# print(content_format % (item_width, 'Apples', price_width, 0.4))
# print(content_format % (item_width, 'Dried Apricots (16 oz.)', price_width, 2))

# ============================
# people = {
#     'Alice': {'phone': '1234', 'addr': 'Foo drive 33'},
#     'Beth': {'phone': '4321', 'addr': 'Bar street 32'},
#     'Cecil': {'phone': '3158', 'addr': 'Baz avenue 55'}
# }
#
# labels = {
#     'phone': 'phone number', 'addr': 'address'
# }
#
# name = input('Name: ')
#
# request = input('Phone(p) or Address(a)?')
#
# if request == 'p':
#     key = 'phone'
# elif request == 'a':
#     key = 'addr'
# if name in people:
#     print("%s's %s is %s" % (name, labels[key], people[name][key]))

# ======================
# girls = ['abbe', 'alice', 'bernice', 'clarice', 'abc']
# boys = ['chris', 'arnold', 'bob', 'alex', 'aef']
# letter_girls = {}
# for girl in girls:
#     letter_girls.setdefault(girl[0], []).append(girl)
# # print([b + '==' + g for b in boys for g in letter_girls[b[0]]])
# for b in boys:
#     print(b + '==' + letter_girls[b[0]][0])
#     letter_girls[b[0]].pop(0)

# =======================
# my_name = {}
#
#
# def init(data):
#     data['first'] = {}
#     data['middle'] = {}
#     data['last'] = {}
#
#
# def lookup(data, label, name):
#     return data[label].get(name)
#
#
# def store(data, *full_names):
#     for full_name in full_names:
#         names = full_name.split()
#         if len(names) == 2:
#             names.insert(1, '').
#         labels = 'first', 'middle', 'last'
#         for label, name in zip(labels, names):
#             people = lookup(data, label, name)
#             # print(people)
#             if people:
#                 people.append(full_name)
#                 # pass
#             else:
#                 data[label][name] = [full_name]
#
#
# init(my_name)
# store(my_name, 'Robin Hood')
# # print(my_name)
# store(my_name, 'Robin Locksley')
# # print(lookup(my_name, 'last', 'Hood'))
# print(my_name)


# ========================
# def check_index(key):
#     if not isinstance(key, int):
#         raise TypeError
#     if key < 0:
#         raise IndexError
#
#
# class ArithmeticSequence:
#     def __init__(self, start=0, step=1):
#         self.start = start
#         self.step = step
#         self.changed = {}
#
#     def __getitem__(self, key):
#         check_index(key)
#         try:
#             return self.changed[key]
#         except KeyError:
#             return self.start + key * self.step
#             # print('not changed')
#
#     def __setitem__(self, key, value):
#         check_index(key)
#         self.changed[key] = value
#
# s = ArithmeticSequence(1, 2)
# print(s[4])
#
# s[4] = 2
# print(s[4])
# print(s[5])


# ===========================
# test_str = ['foo', ['bar', ['baz']]]
# test = [[1, 2], 3, 4, [5, [6, 7]], 8]
#
#
# def flatten(nested):
#     try:
#         try:
#             nested + ''
#         except TypeError:
#             print('except branch')
#             pass
#         else:
#             print('else branch')
#             raise TypeError('Raised here')
#         for sublist in nested:
#             print('now here')
#             for element in flatten(sublist):
#                 yield element
#     except TypeError as error:
#         print('first try')
#         print(error)
#         yield nested
#
# print(list(flatten(test_str)))
# print(list(flatten(test)))


# =============================
# http://www.cnblogs.com/nima/p/3972593.html
# def conflict(state, col):
#     row = len(state)
#     for i in range(row):
#         if abs(state[i]-col) in (0, row-i):
#             return True
#     return False
#
#
# def queens(num=4, state=()):
#     for pos in range(num):
#         if not conflict(state, pos):
#             if len(state) == num - 1:
#                 yield (pos,)
#             else:
#                 for result in queens(num, state + (pos,)):
#                     yield (pos,) + result
#
# for ss in queens(4):
#     print(ss)


# =============================
# import hashlib
#
#
# def md5_encode(ori_str):
#     hash_md5 = hashlib.md5()
#     hash_md5.update(ori_str.encode('utf-8'))  # Unicode-objects must be encoded before hashing
#     return hash_md5.hexdigest()
# print(md5_encode('123456'))


# ==============================
# import random
#
# test = [1, 2, 3, 4, 5, 6]
# random.shuffle(test)
# while test:
#     input(test.pop())


# ===============================
# import json
# from urllib.parse import urlencode
#
#
# json_list = '{"ids": ["855078ec426348fab77b72d969002e51", "227160e5b2ff443ba31456444260f154"]}'
# json_normal = '{"cartId": "c6ee1eea390446d4a635b053a32e7d7c", "addressid": "fce65ff73eb04cfe99d20646461b9e57"}'
# test = '{"message":null,"success":true,"jumpUrl":"//success.jd.com/success/success.action?orderId=59614423053"}'
# request_data = urlencode(json.loads(json_normal), True)
#
# print(json.loads(test)['jumpUrl'].split('=')[-1])


# # ===============================
# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.select import Select
# import time
#
# SELECT_BY_INDEX = Select(s).select_by_index(1)
#
# driver = webdriver.Chrome()
# url = 'https://www.baidu.com/'
# driver.get(url)
# driver.implicitly_wait(5)
# mouse = driver.find_element_by_link_text('设置')
# ActionChains(driver).move_to_element(mouse).perform()
# time.sleep(2)
# driver.find_element_by_link_text('搜索设置').click()
# s = driver.find_element_by_id('nr')
# time.sleep(2)

# print('正在提交订单，支付方式为' + ('“线下付款”' if True is True else '"xxx"'))

# import base64
#
# s = 'MTA3LjE4MS4xNTQuMjo0NDM6b3JpZ2luOmFlcy0yNTYtY2ZiOnBsYWluOlozSmxZWFJtZFdOcmFX' \
#     'NW5kMkZzYkEvP29iZnNwYXJhbT0mcmVtYXJrcz1ZV3h3YUdFM05qZyZncm91cD1RVXhN'
#
# print(base64.b64decode(s))

# import sys
#
# for arg in sys.argv[1:]:
#     print(arg)

# import time
# # print current time only
# print(time.strftime('%H:%M:%S'))

# import requests
#
# url = 'http://www.108j.club/pic/133/1.jpg'
# r = requests.head(url)
# print(r.headers['content-length'])

from Others.tools import *

make_folder('D:\Download', 'game')
print(os.getcwd())
make_folder(os.path.pardir, 'of')












































