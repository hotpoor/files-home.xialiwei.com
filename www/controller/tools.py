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
import copy

import tornado.escape
from tornado.escape import json_encode, json_decode


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/vendor/')

from tornado.concurrent import Future


from setting import settings
from setting import conn
from setting import cur

from block import get_block,create_block,update_block

from .data import DataWebSocket

class PlayVideoAPIHandler(tornado.web.RequestHandler):
    def post(self):
        aim_id = self.get_argument("aim_id","INROOM")
        msgtype = "VIDEO_PLAY"
        self.finish({"info":"ok"})
        msg = [msgtype, {
            "content": "video_play",
        }, aim_id]
        DataWebSocket.send_to_all(json_encode(msg))

class JsonBlockAPIHandler(tornado.web.RequestHandler):
    def get(self):
        block_id = self.get_argument("block_id",None)
        block = get_block(block_id)
        if not block:
            self.finish({"info":"error","about":"no block","block":block})
            return
        self.finish({"info":"ok","about":"success","block":block})


class CreateBlockAPIHandler(tornado.web.RequestHandler):
    def post(self):
        block = self.get_argument("block","{}")
        block = json_decode(block)
        [new_block_id,new_block]=create_block(block)
        self.finish({
            "info":"ok",
            "about":"create success",
            "block":new_block,
            "block_id":new_block_id
            })
class UpdateBlockAPIHandler(tornado.web.RequestHandler):
    def post(self):
        block_id = self.get_argument("block_id",None)
        block = self.get_argument("block","{}")
        block = json_decode(block)
        token = self.get_argument("token",None)
        if token not in ["developer"]:
            self.finish({"info":"error","about":"not developer"})
            return
        old_block = get_block(block_id)
        old_block_data = copy.deepcopy(old_block.get("old_block_data",[]))
        
        if len(old_block_data)==0:
            old_block_data.insert(0,old_block)
        else:
            del old_block["old_block_data"]
            old_block_data.insert(0,old_block)
        block["old_block_data"]=old_block_data
        block["updatetime"]=time.time()
        update_block(block_id,block)
        self.finish({
            "info":"ok",
            "about":"big update success",
            "block":block,
            "block_id":block_id
            })