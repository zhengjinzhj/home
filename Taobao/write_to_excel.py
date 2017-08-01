# -*- coding:utf-8 -*-

import xlrd
import xlwt
from xlutils.copy import copy
import config


def new_excel(out_file=config.OUT_FILE):
    print '发现写入目标不存在，正在创建文件:', out_file
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    book.add_sheet('out_file', cell_overwrite_ok=True)
    book.save(out_file)
    print '已成功创建文件', out_file


def repeat_excel(word, out_file=config.OUT_FILE):
    word = word.encode('utf-8')
    print '正在检测"%s"是否存在于文件中' % word
    try:
        workbook = xlrd.open_workbook(out_file)
        sheet = workbook.sheet_by_index(0)
        words = sheet.col_values(0)
        if word in words:
            print '用户名"%s"在excel中已经存在,跳过该用户' % word
            return True
        else:
            print '用户名"%s"在excel中不存在' % word
            return False
    except IOError, e:
        if 'No such file' in e.strerror:
            print '匹配重复时未找到OUT_FILE文件', out_file
            new_excel(out_file)
            return False
        return False


def write_to_excel(contents, out_file=config.OUT_FILE):
    print '正在写入到文本中', contents[0]
    try:
        rb = xlrd.open_workbook(out_file)
        sheet = rb.sheets()[0]
        row = sheet.nrows
        wb = copy(rb)
        sheet = wb.get_sheet(0)
        count = 0
        name = contents[0]
        if not repeat_excel(name, out_file):
            for content in contents:
                sheet.write(row, count, content)
                count += 1
                wb.save(out_file)
                print '已成功写入到文件%s第%d行' % (out_file, count+1)
        else:
            print '内容已存在, 跳过写入文件', out_file
    except IOError:
        print '未找到该文件', out_file
        new_excel(out_file)
        write_to_excel(contents, out_file)


def write_info(info, out_file=config.OUT_FILE):
    if len(info) >= 3:
        name = info[0].encode('utf-8')
        print '准备将%s写入文件' % name
        comment = info[1]
        url = info[2]
        contents = (name, comment, url)
        write_to_excel(contents, out_file)
    else:
        print '写入文件时发生错误，跳过写入'


def get_count():
    try:
        with open(config.COUNT_FILE, 'r') as f:
            page = f.read()
            if not page:
                return 0
            else:
                return page
    except Exception:
        print '不存在计数文件，可从开头开始抓取'
        return 0


def write_count(count, out_file):
    try:
        with open(out_file, 'w') as f:
            f.write(str(count))
            f.close()
    except TypeError:
        print '页码写入失败'


























