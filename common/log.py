#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author : Liangdong Zhang
# @date : 2020/6/28 17:37
# @file : log.py
import os
import logging
import time

# 根据执行情况，如有必要则再次封装

class logger:

    lf = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    reslutpath = os.path.join(os.path.join(lf, "result"))
    if not os.path.exists(reslutpath):
        os.mkdir(reslutpath)
    logpath = os.path.join(reslutpath, "log")
    if not os.path.exists(logpath):
        os.mkdir(logpath)
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    format = logging.Formatter('[%(asctime)s][%(name)s][%(filename)s][%(levelname)s]:%(message)s')
    handler = logging.FileHandler(os.path.join(logpath, "execute.log"))
    handler.setFormatter(format)
    log.addHandler(handler)


    def get_logger(self):
        return self.log

    @classmethod
    def exception(cls,msg):
        cls.log.exception(msg)
        return

    @classmethod
    def critical(cls,msg):
        cls.log.critical(msg)

    @classmethod
    def error(cls,msg):
        cls.log.error(msg)
        return

    @classmethod
    def info(cls,msg):
        cls.log.info(msg)
        return

    @classmethod
    def warning(cls,msg):
        cls.log.warning(msg)
        return










