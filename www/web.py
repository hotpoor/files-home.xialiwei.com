#!/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import asyncio
import tornado.ioloop
import tornado.web
import tornado.log
import sqlite3

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/vendor/')

from setting import settings
from controller import files_upload
from controller import tools
from controller import data_tcp
from controller import data

tornado.log.enable_pretty_logging()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class StaticFileHandler(tornado.web.StaticFileHandler):
    async def set_default_headers(self):
        # 设置 CORS 头部允许所有域名访问
        self.set_header("Access-Control-Allow-Origin", "*")
        # 其他 CORS 头部设置
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
        self.set_header('Access-Control-Max-Age', '3600')
        # 允许浏览器存储 OPTIONS 请求的响应，以便在将来的请求中重用它
        self.set_header('Access-Control-Allow-Credentials', 'true')
class Video(tornado.web.RequestHandler):
    async def get(self):
        self.render("template/video.html")
        # self.redirect("/static/uploads_local/abc8e4d7706b7fd9ed1bf09f8061d243")

class VideoSmallRoom(tornado.web.RequestHandler):
    async def get(self):
        self.video_uri = "http://192.168.200.5/video/b.mp4"
        self.version = settings["version"]
        self.render("template/video_small_room.html")
        # self.redirect("/static/uploads_local/abc8e4d7706b7fd9ed1bf09f8061d243")
class VideoSmallRoomLeft(tornado.web.RequestHandler):
    async def get(self):
        self.video_uri = "http://192.168.200.5/video/b_l.mp4"
        self.version = settings["version"]
        self.render("template/video_small_room.html")
        # self.redirect("/static/uploads_local/abc8e4d7706b7fd9ed1bf09f8061d243")
class VideoSmallRoomRight(tornado.web.RequestHandler):
    async def get(self):
        self.video_uri = "http://192.168.200.5/video/b_r.mp4"
        self.version = settings["version"]
        self.render("template/video_small_room.html")
        # self.redirect("/static/uploads_local/abc8e4d7706b7fd9ed1bf09f8061d243")

def make_app():
    return tornado.web.Application([
        # (r"/api/upload_stream", files_upload.UploadStreamHandler,dict(upload_dir=settings["source_path"])),

        (r"/api/block/create",tools.CreateBlockAPIHandler),
        (r"/api/block/update",tools.UpdateBlockAPIHandler),
        (r"/api/upload/list", files_upload.ListUploadAPIHandler),
        (r"/api/upload/check", files_upload.CheckUploadAPIHandler),
        (r"/api/upload", files_upload.UploadAPIHandler,dict(upload_dir=settings["source_path"])),
        (r"/upload_file", files_upload.UploadFilePage),
        (r"/static/(.*)", StaticFileHandler, {"path": settings["static_path"]}),
        (r"/api/data/json",tools.JsonBlockAPIHandler),

        (r"/video_small_room",VideoSmallRoom),
        (r"/vsrl",VideoSmallRoomLeft),
        (r"/vsrr",VideoSmallRoomRight),
        (r"/video",Video),


        (r"/tcp_dashboard",data_tcp.TCPDashboardHandler),
        (r"/api/tcp_send",data_tcp.TCPSendAPIHandler),

        (r"/api/udp_send",data_tcp.UDPSendAPIHandler),

        (r"/api/play_video",tools.PlayVideoAPIHandler),
        (r"/ws",data.DataWebSocket),

        (r"/", MainHandler),
    ], **settings)

async def main():
    tcpserver = data_tcp.TCPHandler()
    # 8002属于threejs
    tcpserver.listen(8003)

    app = make_app()
    app.listen(settings["wss_port"],max_body_size=settings["max_body_size"],max_buffer_size=settings["max_buffer_size"])
    print("Server started at http://localhost:%s"%settings["wss_port"])
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
    tornado.ioloop.IOLoop.current().start()
