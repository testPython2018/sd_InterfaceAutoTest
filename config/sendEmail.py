#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author : Liangdong Zhang
# @date : 2020/6/28 17:37
# @file : sendEmail.py

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from datetime import datetime
import threading
import config.readConfig as readConfig
localReadConfig = readConfig.Config()

class Email:
    def __init__(self):
        global smtp_addr, password, from_addr, to_addrs, subject, content
        smtp_addr = localReadConfig.get_email("smtp_addr")
        password = localReadConfig.get_email("password")
        from_addr = localReadConfig.get_email("from_addr")
        self.value = localReadConfig.get_email("to_addrs")
        title = localReadConfig.get_email("subject")
        content = localReadConfig.get_email("content")

        self.to_addr = []

        self.to_addr = str(self.value).split(";")

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.subject = title + " " + date

        self.msg = MIMEMultipart('mixed')

    def config_header(self):
        self.msg['subject'] =self.subject
        self.msg['from'] = from_addr


    def config_content(self):

        f = open(os.path.join(os.path.abspath(os.curdir),'config',"emailStyle.txt"),encoding='utf-8')

        content = f.read()
        f.close()
        content_plain = MIMEText(content, 'html', 'utf-8')
        self.msg.attach(content_plain)
        self.config_image()

    def config_image(self):

        image1_path = os.path.join(os.path.abspath(os.curdir),'config','logo.png')
        fp1 = open(image1_path, 'rb')
        msgImage1 = MIMEImage(fp1.read())
        fp1.close()

        msgImage1.add_header('Content-ID', '<image1>')
        self.msg.attach(msgImage1)

        image2_path = os.path.join(os.path.abspath(os.curdir),'config', 'erweima.png')
        fp2 = open(image2_path, 'rb')
        msgImage2 = MIMEImage(fp2.read())
        fp2.close()

        msgImage2.add_header('Content-ID', '<image2>')
        self.msg.attach(msgImage2)

    def config_file(self,file):

        if file is not None:
            filename=file
        else:
            filename = 'NoData'

        try:


            zippath = os.path.join(os.path.dirname(os.path.dirname(__file__)),filename)

            reportfile = open(zippath, 'rb').read()
            filehtml=MIMEApplication(reportfile)

            filehtml['Content-Type'] = 'application/octet-stream'
            filehtml['Content-Disposition'] = 'attachment;filename="'+filename+'"'
            self.msg.attach(filehtml)

        except IOError:
            msg="sorry,the file "+filename+" does not exist!"
            print(msg)



    def send_email(self,file):
        self.config_header()
        self.config_content()
        self.config_file(file)
        try:
            smtp = smtplib.SMTP()
            smtp.connect(smtp_addr,port=25)
            # #Linux下请用SMTP_SSL方法
            # smtp = smtplib.SMTP_SSL(host=smtp_addr)
            # smtp.connect(host=smtp_addr,port=465)
            smtp.login(from_addr, password)
            smtp.sendmail(from_addr, self.to_addr, self.msg.as_string())
            smtp.quit()
        except Exception as ex:
            print("[error]" + str(ex))

class MyEmail:
    email = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_email():
        if MyEmail.email is None:
            MyEmail.mutex.acquire()
            MyEmail.email = Email()
            MyEmail.mutex.release()
        return MyEmail.email

