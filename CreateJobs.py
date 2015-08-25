# -*- coding:utf-8 -*-
__author__ = 'Boss'

from redis import Redis
from rq import Queue
from ParseJobInfo import parse_jobinfo
import xlrd


#连接redis
redis_conn = Redis(host='192.168.0.108', port=6379)
q = Queue(connection=redis_conn, async=True)  # 设置async为False则入队后会自己执行 不用调用perform

book = xlrd.open_workbook('1.xlsx')
table = book.sheet_by_index(0)
rows = table.nrows

for i in range(rows):
    row = table.row_values(i)
    job = q.enqueue(parse_jobinfo, row)
    print job.id
