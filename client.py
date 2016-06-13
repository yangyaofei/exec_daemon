#!/usr/bin/python
# coding:utf-8
import sockets
import logging

logging.basicConfig(level=logging.INFO)
s = sockets.connectServer()
exe = "mkdir /var/lib/test/ddd"
logging.info(exe)
exe = "[exec]" + exe
s.send(exe)
result = sockets.recv(s)
logging.info(result)
s.close()
