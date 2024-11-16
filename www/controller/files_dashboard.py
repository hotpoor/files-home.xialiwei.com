#!/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import asyncio
import tornado.ioloop
import tornado.web
import tornado.concurrent
import sqlite3
import time
import re
import hashlib


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/vendor/')

from tornado.concurrent import Future


from setting import settings
from setting import conn
from setting import cur

class FilesDashbaordTCPHandler(tornado.web.RequestHandler):
    def get(self):
        self.version = settings["version"]
        self.render("../template/upload_file.html")  # 渲染上传页面














