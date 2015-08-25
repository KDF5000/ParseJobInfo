#-*-coding:utf-8-*-
__author__ = 'Boss'
import re

def take_first(tp):
    if tp is None:
        return None
    for value in tp:
        if value is not None:
            return value.decode("utf-8")
    return None


str = "性质外资（非欧美）发布时间2015/08/20薪资2000-2999/月工作地点广州-越秀区招聘10人 | 学历不限 | 工作经验不限 | 普通话"

s1 = r".*性质([\w\s\W]+)发布时间|.*性质([\w\s\W]+)工作地点|.*性质([\w\s\W]+)招聘|.*性质([\w\s\W]+)$"

s2 = r".*发布时间([\d\s/]+)薪资|.*发布时间([\d\s/]+)工作地点|" \
     r".*发布时间([\d\s/]+)招聘|.*发布时间([\d\s/]+)$"

s3 = r".*薪资([\w\s\W]+)工作地点|.*薪资([\w\s\W]+)招聘|.*薪资([\w\s\W]+)$"

s4 = r".*工作地点([\W\w\s-]+)招聘|.*工作地点([\W\w\s-]+)$"

s5 = r".*招聘([\d\W\w\s|]+)$"

res1 = re.match(s1, str)
res2 = re.match(s2, str)
res3 = re.match(s3, str)
res4 = re.match(s4, str)
res5 = re.match(s5, str)

print take_first(res1.groups() if res1 else res1)
print take_first(res2.groups() if res2 else res2)
print take_first(res3.groups() if res3 else res3)
print take_first(res4.groups() if res4 else res4)
print take_first(res5.groups() if res5 else res5)



