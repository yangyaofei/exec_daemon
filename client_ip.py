#!/usr/bin/python
# coding:utf-8
import sockets
import logging

logging.basicConfig(level=logging.INFO)
s = sockets.connectServer()
ip_c_null = "null"
ip_c = "192.168.1.3|255.255.255.0|192.168.1.1"
logging.info(ip_c_null)
ip = "[ip]" + ip_c_null
s.send(ip)
result = sockets.recv(s)
logging.info(result)
s.close()
