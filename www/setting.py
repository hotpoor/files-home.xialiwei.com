#!/bin/env python
#coding=utf-8
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/vendor/')
#os.chdir(os.path.dirname(os.path.abspath(__file__)))

import logging
import uuid

import sqlite3

from version import version_num

settings = {
    "static_path": os.path.join(os.path.dirname(__file__),"static"),
    "cookie_secret": "hotpoorinchina",
    "cookie_domain": "",
    # "debug":True,
    "debug":False,
    "wss_port":8888,
    "tcp_port":8003,
    

    # "source_path":"/media/xialiwei/WD_4T_1/files-home.xialiwei.com",
    
    # "source_path":"static/uploads",
    # "source_db":"sqlite_db/files-home.db",

    "source_path":"static/uploads_local",
    "source_db":"sqlite_db_local/files-home.db",
    "max_body_size":1024*1024*1024*100,
    "max_buffer_size":1024*1024*100,
    "version":version_num,
}

conn = sqlite3.connect(settings["source_db"])
cur = conn.cursor()
try:
    result_files = cur.execute("SELECT count(1) FROM index_files")
    print(result_files.fetchall())
except:
    print("no index_files, create")
    cur.execute("CREATE TABLE index_files(md5,filename,createtime,updatetime,size,real_path,thumbnail,type,entity_id)")
try:
    result_entities = cur.execute("SELECT count(1) FROM entities")
    print(result_entities.fetchall())
except:
    print("no entities, create")
    cur.execute("CREATE TABLE entities(id,body,createtime,updatetime)")
try:
    result_search = cur.execute("SELECT count(1) FROM index_search")
    print(result_search.fetchall())
except:
    print("no index_search, create")
    cur.execute("CREATE TABLE index_search(word,entity_id)")
