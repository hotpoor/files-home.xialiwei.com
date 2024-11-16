#!/bin/env python
#coding=utf-8
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/vendor/')
#os.chdir(os.path.dirname(os.path.abspath(__file__)))

import logging
import uuid
import datetime
import sqlite3
import json

from setting import settings
from setting import conn
from setting import cur

import time

def new_key():
    while True:
        block_id = uuid.uuid4().hex
        result = cur.execute("SELECT * FROM entities WHERE id=?",(block_id,))
        result_columns = [description[0] for description in cur.description]
        result = result.fetchall()
        if not result:
            break
    return block_id
def _pack(data): return json.dumps(data, ensure_ascii=False)
def _unpack(data): return json.loads(data or "{}")

def get_block(block_id):
    result = cur.execute("SELECT * FROM entities WHERE id=?",(block_id,))
    result_columns = [description[0] for description in cur.description]
    result = result.fetchall()
    result_json = {}
    if not result:
        return None
    for i in range(0,len(result_columns)):
        result_json[result_columns[i]]=result[0][i]
    block = _unpack(result_json["body"])
    return block

def create_block(block):
    block_id = new_key()
    current_time = time.time()
    block["type"] = "block"
    block["owner"]=block.get("owner",None)
    block["datetime"] = datetime.datetime.now().isoformat()
    block["createtime"]=current_time
    block["updatetime"]=current_time

    cur.execute("INSERT INTO entities(id,body,createtime,updatetime) VALUES(?,?,?,?)",(block_id,_pack(block),current_time,current_time))
    conn.commit()
    return [block_id,block]
def update_block(block_id,block):
    current_time = time.time()
    cur.execute("UPDATE entities SET body=? , updatetime=? WHERE id=?",(_pack(block),current_time,block_id))
    conn.commit()

