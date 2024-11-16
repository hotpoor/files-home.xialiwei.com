# -*- coding: utf-8 -*-
import sys
import os
import os.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/vendor/')
import uuid
import time
import random
import string
import hashlib
import urllib
import copy
from functools import partial
import logging
import datetime

import tornado
import tornado.web
import tornado.escape
import tornado.websocket
import tornado.httpclient
import tornado.gen
from tornado.escape import json_encode, json_decode

# from user_agents import parse as uaparse #早年KJ用来判断设备使用

# import nomagic
# from nomagic.cache import get_user, get_users, update_user, get_doc, get_docs, update_doc, get_aim, get_aims, update_aim, get_entity, get_entities, update_entity
# from nomagic.cache import BIG_CACHE
from setting import settings
from setting import conn

from .base import WebRequest
from .base import WebSocket

from tornado.tcpserver import TCPServer
import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# class TCPConnection(object):
#     tcpclients = set()
#     def __init__(self, stream, address):
#         TCPConnection.tcpclients.add(self)
#         self._stream = stream
#         self._address = address
#         self._stream.set_close_callback(self.on_close)
#         self.read_message()
#         print("A new user has entered the chat room.", address)
#     # @tornado.gen.coroutine
#     # def post_mmplus(self, data):
#     #     print "---"
#     #     print data
#     #     http_client = tornado.httpclient.AsyncHTTPClient()
#     #     url = "http://www.hotpoor.org/api/comment/submit_data"
#     #     headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
#     #     params = {
#     #         "user_id":"0cd8429c1da249b6935d7eef72d7fc0b",
#     #         "aim_id":"0cd8429c1da249b6935d7eef72d7fc0b",
#     #         "app":"hotpoor",
#     #         "content":data,
#     #     }
#     #     body = urllib.urlencode(params)
#     #     request = tornado.httpclient.HTTPRequest(
#     #                 url = url,
#     #                 method = "POST",
#     #                 body = body,
#     #                 headers = headers,
#     #                 validate_cert = False)
#     #     response = yield http_client.fetch(request)
#     #     print response.body
#     def read_message(self):
#         self._stream.read_until('\n', self.broadcast_messages)

#     def broadcast_messages(self, data):
#         print("---")
#         print("User said:", data[:-1], self._address)

#         data_json = json_decode(data[:-1])
#         if data_json.get("msg_type",None) in ["heart"]:
#             data_json["heart"]+=1
#             self.send_message(json_encode(data_json)+"\n")
#     #     # print data
#     #     # self.post_mmplus(data)
#     #     # for tcpconn in TCPConnection.tcpclients:
#     #     #     tcpconn.send_message(data)
#         self.read_message()

#     def send_message(self, data):
#         self._stream.write(data)

#     def on_close(self):
#         print("A user has left the chat room.", self._address)
#         TCPConnection.tcpclients.remove(self)
class TCPDashboardHandler(WebRequest):
    def get(self):
        self.time_now = time.time()
        self.tcpclients_dict_key = list(TCPHandler.tcpclients_dict.keys())
        self.render("../template/tcp_dashboard.html")
class TCPSendAPIHandler(WebRequest):
    async def post(self):
        msssage = self.get_argument("message","{}")
        device_id = self.get_argument("device_id","")

        need_handlers = TCPHandler.tcpclients_dict.get(device_id,[])
        print("TCPHandler.tcpclients_dict",TCPHandler.tcpclients_dict)
        print("%s need_handlers"%(device_id),need_handlers)
        for need_handler in need_handlers:
            message_all = "%sHHH"%msssage
            # await need_handler._stream.write(message_all.encode())
            await need_handler.stream.write(message_all.encode())
class UDPSendAPIHandler(WebRequest):
    async def post(self):
        action = self.get_argument("action","")
        device_id = self.get_argument("device_id","")
        try:
            device_id_ip = int(device_id)+100
            url = "192.168.200.%s"%device_id_ip
        except:
            self.finish({"info":"error","about":"error","url":url})
            return
        server_address = (url, 8090)
        if action in ["down"]:
            server_socket.sendto(b"STOP",server_address)
            time.sleep(0.1)
            print("stop")
            server_socket.sendto(b"LOW",server_address)
            print("low")
        elif action in ["center"]:
            server_socket.sendto(b"STOP",server_address)
            time.sleep(0.1)
            print("stop")
            server_socket.sendto(b"MID",server_address)
            print("mid")
        elif action in ["all_start","start"]:
            server_socket.sendto(b"START",server_address)
        elif action in ["all_stop","stop"]:
            server_socket.sendto(b"STOP",server_address)
        elif action in ["all_fanlow","fanlow"]:
            server_socket.sendto(b"FANLOW",server_address)
        elif action in ["all_fanhigh","fanhigh"]:
            server_socket.sendto(b"FANHIGH",server_address)
        elif action in ["all_fanstop","fanstop"]:
            server_socket.sendto(b"FANSTOP",server_address)
        elif action in ["all_turnstart","turnstart"]:
            server_socket.sendto(b"TURNSTART",server_address)
        elif action in ["all_turnstop","turnstop"]:
            server_socket.sendto(b"TURNSTOP",server_address)
            time.sleep(0.1)
            server_socket.sendto(b"STOP",server_address)
        elif action in ["all_virbon","virbon"]:
            # server_socket.sendto(b"START",server_address)
            # time.sleep(0.1)
            server_socket.sendto(b"VIRBON",server_address)
            print("VIRBON",server_address)
        elif action in ["all_virboff","virboff"]:
            # server_socket.sendto(b"STOP",server_address)
            # time.sleep(0.1)
            server_socket.sendto(b"VIRBOFF",server_address)
            print("VIRBOFF",server_address)
        self.finish({"info":"ok","about":"success","url":url})

class TCPConnection:
    def __init__(self, stream, address):
        self.stream = stream
        self.address = address

    def __del__(self):
        print(f"Connection {self.address} closed")


class TCPHandler(TCPServer):
    def __init__(self, *args, **kwargs):
        super(TCPHandler, self).__init__(*args, **kwargs)
        self.tcpclients = set()
        self.tcpclients_dict = {}
    tcpclients = set()
    tcpclients_dict = {}

    # def handle_stream(self, stream, address):
    #     print("New connection :", address, stream)
    #     TCPConnection(stream, address)
    #     print("connection num is:", len(TCPConnection.tcpclients))
    async def handle_stream(self, stream, address):
        handler = TCPConnection(stream, address)
        print("handler")
        print(handler)
        # self._stream = stream
        print(f"New connection from {address}")
        TCPHandler.tcpclients.add(handler)
        while True:
            try:
                # 读取客户端发送的数据
                data = await stream.read_until(b'HHH')
                print("data",data)
                try:
                    # 尝试用 utf-8 解码数据
                    message = data.decode('utf-8').strip()
                    print(f"Received: {message} from {address}")
                    message = message.replace("HHH","")
                    message_json = json_decode(message)
                    device_id = message_json.get("device_id",None)
                    device_id_handlers = TCPHandler.tcpclients_dict.get(device_id,[])
                    if handler not in device_id_handlers:
                        device_id_handlers.insert(0,handler)
                        TCPHandler.tcpclients_dict[device_id]=device_id_handlers
                except UnicodeDecodeError:
                    # 如果解码失败，打印原始数据
                    print(f"Received undecodable data from {address}: {data}")

                # 回应数据给客户端
                # play,pause,start,return
                await stream.write(b'{"in_game":"heart"}HHH')
            except tornado.iostream.StreamClosedError:
                print(f"Connection closed by {address}")
                TCPHandler.tcpclients.remove(handler)
                for k,v in TCPHandler.tcpclients_dict.items():
                    if handler in v:
                        v.remove(handler)
                        TCPHandler.tcpclients_dict[k]=v
                break
    
