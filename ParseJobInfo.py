#-*- coding:utf-8 -*-
__author__ = 'Boss'

import xlrd
import re
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')


hot_keys = [u'职位描述', u'职位标签', u'福利待遇', u'上班地址']
filter_line = [u"", u"显示全部", u'查看地图', u"交通路线", u"附近环境", u"举报职位"]

kv_rel = {u'职位描述': 'position_des', u'职位标签': 'position_tag',
          u'福利待遇': 'benefits', u'上班地址': 'work_address'}


# 职位要求信息正则表达式
s1 = r".*性质([\w\s\W]+)发布时间|.*性质([\w\s\W]+)工作地点|.*性质([\w\s\W]+)招聘|.*性质([\w\s\W]+)$"

s2 = r".*发布时间([\d\s/]+)薪资|.*发布时间([\d\s/]+)工作地点|" \
     r".*发布时间([\d\s/]+)招聘|.*发布时间([\d\s/]+)$"

s3 = r".*薪资([\w\s\W]+)工作地点|.*薪资([\w\s\W]+)招聘|.*薪资([\w\s\W]+)$"

s4 = r".*工作地点([\W\w\s-]+)招聘|.*工作地点([\W\w\s-]+)$"

s5 = r".*招聘([\d\W\w\s|]+)$"

# 取一个tuple或者list的第一个部位None的元素
def take_first(tp):
    if tp is None:
        return None
    for value in tp:
        if value is not None:
            return value.decode("utf-8")
    return None

#从excel一行数据提取需要的数据
def extract_data(row_data):
    data_dict = dict()
    all_info = row_data[8]
    data_dict['source_url'] = row_data[0]
    data = all_info.strip()
    data_set = data.split('\n')
    res_data = []
    with open('o.txt', 'w') as f:
        for value in data_set:
            data = value.strip()
            if data not in filter_line:
                res_data.append(data)
                #f.write(data.encode('utf-8')+'\n')

    # 取前三个正常的
    data_dict['position'] = res_data[0]  # 招聘职位
    data_dict['company'] = res_data[1]  # 招聘公司
    # 性质民营公司发布时间2015/08/20工作地点广州-越秀区招聘3人 | 大专 | 2年工作经验 | 英语 熟练 | 普通话 良好
    position_info = res_data[2].encode('utf-8')  # 职位的相关信息

    res1 = re.match(s1, position_info)
    res2 = re.match(s2, position_info)
    res3 = re.match(s3, position_info)
    res4 = re.match(s4, position_info)
    res5 = re.match(s5, position_info)
    data_dict['company_type'] = take_first(res1.groups() if res1 else res1)
    data_dict['post_time'] = take_first(res2.groups() if res2 else res2)
    data_dict['salary'] = take_first(res3.groups() if res3 else res3)
    data_dict['work_address'] = take_first(res4.groups() if res4 else res4)
    data_dict['hunt_required'] = take_first(res5.groups() if res5 else res5)

    for hot_key in hot_keys:
        if hot_key in res_data:
            index = res_data.index(hot_key)
            for val in res_data[index+1:]:
                if val in hot_keys:
                    break
                data_key = kv_rel[hot_key]
                if data_key not in data_dict.keys() or data_dict[data_key] is None:
                    data_dict[data_key] = ""
                data_dict[data_key] += val
    return data_dict


def insert_db(data_dict):
    if data_dict is None or len(data_dict.keys()) == 0:
        print '>>>>>Empty data!'
        return None

    conn = MySQLdb.connect(host="192.168.0.107", user="root", passwd="root123", db="haolaoban", charset="utf8")
    cursor = conn.cursor()
    sql = "insert into job_info("
    values = []
    sql_vals = " values("
    for k, v in data_dict.iteritems():
        if v is None:
            data_dict[k] = ""
        sql += k + ','
        sql_vals += "%s,"
        values.append(v)
    sql = sql.strip(',')
    sql_vals = sql_vals.strip(',')

    full_sql = sql + ')' + sql_vals + ')'

    try:
        cursor.execute(full_sql, tuple(values))
        cursor.close()
        conn.commit()
        conn.close()
    except MySQLdb.MySQLError, e:
        try:
            sql_error = "Error %d:%s" % (e.args[0], e.args[1])
            print sql_error
        except IndexError:
            print "MySQL Error:%s" % str(e)
        return None


def parse_jobinfo(data):
    res_dict = extract_data(data)
    try:
        insert_db(res_dict)
        print ">>>>> Insert Successfully!"
    except Exception, e:
        print ">>>>>", e.message
    finally:
        return None

if __name__ == "__main__":
    book = xlrd.open_workbook('1.xlsx')
    table = book.sheet_by_index(0)
    row = table.row_values(28)
    parse_jobinfo(row)
    # res_dict = extract_data(row)
    #
    # for k, v in res_dict.iteritems():
    #     print k, ':', v
    #
    # insert_db(res_dict)









