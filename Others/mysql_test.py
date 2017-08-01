# -*- coding:utf-8 -*-

import MySQLdb

try:
    conn = MySQLdb.Connect(host='localhost', user='root', passwd='123', port=3306)
    cur = conn.cursor()
    cur.execute('create database if not exists test')
    # conn.selcet_db('test')
    cur.execute('use test')
    cur.execute('create table test(id int, info varchar(20))')
    value = [1, 'just for testing']
    cur.execute('insert into test values(%s, %s)', value)
    values = []
    for i in xrange(20):
        values.append((i, 'just for testing' + str(i)))
    cur.executemany('insert into test values(%s, %s)', values)
    cur.execute('update test set info = "value changed" where id=3')
    conn.commit()
    cur.close()
    conn.close()

except MySQLdb.Error, e:
    print e.args[0], e.args[1]







