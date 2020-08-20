# -*- coding: utf-8 -*-


import csv
import datetime
import os
import re
import time
import sys
type = sys.getfilesystemencoding()
import pymysql
import xlrd
import requests
from requests.exceptions import RequestException


def call_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def removeDot(item):
    f_l = []
    for it in item:
        f_str = "".join(it.split(","))
        f_l.append(f_str)

    return f_l


def remove_block(items):
    new_items = []
    for it in items:
        f = "".join(it.split())
        new_items.append(f)
    return new_items


def writerDt_csv(headers, rowsdata):
    # rowsdata列表中的数据元组,也可以是字典数据
    with open('tokyoTSN.csv', 'w',newline = '') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rowsdata)


def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='Yahoo_J',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:

        cursor.executemany('insert into all_jobs (all_job,yp_1000w,yp_800w,yp_500w) values (%s,%s,%s,%s)', content)
        connection.commit()
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass



def all_jobs():
    url = 'https://job.yahoo.co.jp/'
    html = call_page(url)
    patt = re.compile('<div class="searchWrap__ttl">現在の求人総数<strong>(.*?)</strong>.*?</div>')
    item = re.findall(patt,html)
    f_item = removeDot(item)
    big_list.append(f_item)





def yp_tokyo_1000w():
    url = 'https://job.yahoo.co.jp/jobs/?q=&l=%E6%9D%B1%E4%BA%AC%E9%83%BD&su=YAR&smn=10000000&side=1'
    html = call_page(url)
    patt = re.compile('<h1 class="titleArea__title ttl--leftLine"><span>.*?</span>関連の求人検索結果（(.*?)件）</h1>', re.S)
    item = re.findall(patt, html)
    f_item = removeDot(item)
    big_list.append(f_item)




def yp_tokyo_800w():
    url = 'https://job.yahoo.co.jp/jobs/?q=&l=%E6%9D%B1%E4%BA%AC%E9%83%BD&su=YAR&smn=8000000&side=1'
    html = call_page(url)
    patt = re.compile('<h1 class="titleArea__title ttl--leftLine"><span>.*?</span>関連の求人検索結果（(.*?)件）</h1>', re.S)
    item = re.findall(patt, html)
    f_item = removeDot(item)
    big_list.append(f_item)



def yp_tokyo_500w():
    url = 'https://job.yahoo.co.jp/jobs/?q=&l=%E6%9D%B1%E4%BA%AC%E9%83%BD&su=YAR&smn=5000000&side=1'
    html = call_page(url)
    patt = re.compile('<h1 class="titleArea__title ttl--leftLine"><span>.*?</span>関連の求人検索結果（(.*?)件）</h1>', re.S)
    item = re.findall(patt, html)
    f_item = removeDot(item)
    big_list.append(f_item)



if __name__ == '__main__':
    big_list= []
    all_jobs()
    yp_tokyo_1000w()
    yp_tokyo_800w()
    yp_tokyo_500w()
    ff_l = []
    f_tup = tuple(big_list)
    ff_l.append((f_tup))
    print(ff_l)
    print(len(ff_l[0]))
    insertDB(ff_l)




# all_job,yp_1000w,yp_800w,yp_500w
# create table all_jobs(id int not null primary key auto_increment,all_job  float,yp_1000w float,
# yp_800w float,
# yp_500w float,
# LastTime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP) engine=InnoDB  charset=utf8;


# drop table Tokyo_TSN;



