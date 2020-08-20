# !/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import datetime
import pymysql
import pandas as pd

from sqlalchemy import create_engine
import pymysql
import pandas as pd
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import datetime

engine_tsn = create_engine('mysql+pymysql://root:123456@localhost:3306/Yahoo_J')



sql_tsn = 'select LastTime, all_job,yp_1000w,yp_800w,yp_500w  from all_jobs  ; '

ln = os.getcwd()


def savedt():

    df_js225 = pd.read_sql_query(sql_tsn, engine_tsn)
    excelFile3 = '{0}/{1}.xlsx'.format(ln, "all_jobs")  # 处理了文件属于当前目录下！
    df_js225.to_excel(excelFile3)



def sendmail():
    # 发送邮件参数设置
    sender = '291109028@qq.com'  # 发送者邮箱
    password = 'chtrpqnkhyvrcafa'  # 发送者邮箱授权码
    smtp_ip = 'smtp.qq.com'  # smtp服务器ip,根据发送者邮箱而定
    receiver = ['291109028@qq.com']  # 接收者邮箱
    title = 'all_jobs'  # 邮件主题
    content = 'all_jobs'  # 邮件内容
    annex_path = ln  # 报表存储路径，也是附件路径

    try:

        # 传入邮件发送者、接受者、抄送者邮箱以及主题
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = ','.join(receiver)
        message['Subject'] = Header(str(datetime.datetime.now().date()) + title, 'utf-8')

        # 添加邮件内容
        text_content = MIMEText(content)
        message.attach(text_content)

        # 添加附件

        # 首先是xlsx类型的附件

        xlsxpart3 = MIMEApplication(open('{0}/all_jobs.xlsx'.format(ln), 'rb').read())
        xlsxpart3.add_header('Content-Disposition', 'attachment', filename='all_jobs.xlsx')
        message.attach(xlsxpart3)

        # 登入邮箱发送报表
        server = smtplib.SMTP(smtp_ip)  # 端口默认是25,所以不用指定
        server.login(sender, password)
        server.sendmail(sender, receiver, message.as_string())
        server.quit()
        print('success!', datetime.datetime.now())

    except smtplib.SMTPException as e:
        print('error:', e, datetime.datetime.now())  # 打印错误


if __name__ == '__main__':
    savedt()
    sendmail()


##
#6 19 1,15 * *  /usr/local/bin/python3.6 /root/Yahoo_J_Jobs_cron.py
# 2 19  *   *   *   /usr/local/bin/python3.6 /root/Yahoo_J_Jobs_Daily.py