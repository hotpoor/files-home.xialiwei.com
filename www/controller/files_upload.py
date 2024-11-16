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

class UploadFilePage(tornado.web.RequestHandler):
    def get(self):
        self.source_path = settings["source_path"]
        self.version = settings["version"]
        self.render("../template/upload_file.html")  # 渲染上传页面

# @tornado.web.stream_request_body
# class UploadStreamHandler(tornado.web.RequestHandler):
#     def initialize(self, upload_dir):
#         self.upload_dir = upload_dir
#         print("upload_dir",upload_dir)

#     def prepare(self):
#         os.makedirs(self.upload_dir, exist_ok=True)
#         self.file = None
#         self.bytes_received = 0
#         self.total_size = int(self.request.headers.get('Content-Length', 0))
#         # 设置响应头
#         self.set_header("Content-Type", "text/plain")
#         # self.set_header("Transfer-Encoding", "chunked")  # 使用分块传输编码
#         self.write(f"Prepare: Prepare init success.\r\n")
#         self.flush()
#     def data_received(self, chunk):
#         if self.file is None:

#             result = re.search(r'filename="(.+?)"', chunk.decode('utf-8'))
#             if result:
#                 self.file_name = result.group(1)
#                 print("File name is:", self.file_name)
#                 filename = self.file_name

#             filename = self.request.headers.get('X-File-Name', 'uploaded_file')
#             file_path = os.path.join(self.upload_dir, filename)
#             self.file = open(file_path, 'wb')
#         self.file.write(chunk)
#         self.bytes_received += len(chunk)
#         # 计算进度百分比
#         progress = (self.bytes_received / self.total_size) * 100
#         progress_message = f"Progress: {progress:.2f}%\r\n"
#         print("progress_message",progress_message)
#         # 将进度信息写入响应中，并刷新
#         self.write(progress_message)
#         self.flush()
#     @tornado.gen.coroutine
#     def post(self):
#         if self.file:
#             self.file.close()
#         file_name = self.get_body_argument('file_name', None)
#         print("file_name",file_name)
#         self.write(f"Done: File uploaded successfully.\r\n")
#         self.finish()
class ListUploadAPIHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        page_index = int(self.get_argument("page_index","0"))
        page_each = int(self.get_argument("page_each","10"))
        limit = page_each
        offset = page_index*page_each

        result_num = cur.execute("SELECT count(1) FROM index_files")
        result_num = result_num.fetchall()
        if not result_num:
            result_num = 0
        else:
            result_num = result_num[0][0]

        result = cur.execute("SELECT * FROM index_files LIMIT ? OFFSET ?",(limit,offset))
        result_columns = [description[0] for description in cur.description]
        result = result.fetchall()

        self.finish({
            "info":"ok",
            "about":"success",
            "result":result,
            "result_columns":result_columns,
            "files_num":result_num,
        })

class CheckUploadAPIHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        md5 = self.get_argument("md5",None)
        result = cur.execute("SELECT * FROM index_files WHERE md5 in (?)",[md5])
        result_columns = [description[0] for description in cur.description]
        result = result.fetchall()
        if not result:
            self.finish({"info":"ok","about":"success","exist":False})
            return
        self.finish({"info":"ok","about":"success","exist":True})
class UploadAPIHandler(tornado.web.RequestHandler):
    def initialize(self, upload_dir):
        self.upload_dir = upload_dir
        print("upload_dir",upload_dir)
    @tornado.gen.coroutine
    def post(self):
        files = self.request.files.get('files')
        
        if not files:
            self.finish({"info": "error", "about": "No file uploaded"})
            return
        files_info = []
        for file in files:
            for k,v in file.items():
                if k in ["body"]:
                    continue
                print(k,v)
            file_content = file['body']

            filename = file['filename']
            file_size = len(file_content)
            content_type = file['content_type']

            md5_hash = hashlib.md5()
            md5_hash.update(file_content)
            file_md5 = md5_hash.hexdigest()

            result = cur.execute("SELECT * FROM index_files WHERE md5 in (?)",[file_md5])
            result_columns = [description[0] for description in cur.description]
            result = result.fetchall()
            if not result:
                file_path = os.path.join(self.upload_dir, file_md5)
                self.file = open(file_path, 'wb')
                self.file.write(file_content)
                current_time = time.time()
                thumbnail = None
                file_info = {
                    "filename":filename,
                    "file_size":file_size,
                    "file_md5":file_md5,
                    "file_type":content_type,
                    "createtime":current_time,
                    "updatetime":current_time,
                    "real_path":file_path,
                    "thumbnail":thumbnail,
                    "exist":False,
                }
                files_info.append(file_info)
                file_data=[file_md5,filename,current_time,current_time,file_size,file_path,thumbnail,content_type]
                print(file_data)
                cur.execute("INSERT INTO index_files(md5,filename,createtime,updatetime,size,real_path,thumbnail,type) VALUES(?,?,?,?,?,?,?,?)", file_data)
                # cur.execute("INSERT INTO TABLE index_files(md5,filename,createtime,updatetime,size,real_path,thumbnail,type)")
                conn.commit()
            else:
                # print(result_columns)
                # print(result[0])
                file_info = {
                    "filename":result[0][1],
                    "file_size":result[0][4],
                    "file_md5":result[0][0],
                    "file_type":result[0][7],
                    "createtime":result[0][2],
                    "updatetime":result[0][3],
                    "real_path":result[0][5],
                    "thumbnail":result[0][6],
                    "exist":True,
                }
                files_info.append(file_info)

        self.finish({"info":"ok","about":"upload success","files_info":files_info})

