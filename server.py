#!/usr/bin/python
# coding:utf-8
import sockets
import thread
import logging
import commands
import daemon
import sys


def dealClient(conn, addr):
	szBuf = sockets.recv(conn)
	logging.info(szBuf)
	# 检查传递信息
	if szBuf.find("[exec]") != 0:
		conn.close()
		return
	else:
		szBuf = szBuf.replace("[exec]", '')
	# 执行命令
	out = commands.getstatusoutput(szBuf)
	result = ""
	# 获取结果,根据返回值判断是否出错
	if out[0] == 0:
		result = "[resp]" + out[1]
	else:
		result = "[error]" + out[1]
	logging.info(result)
	conn.send(result)
	conn.close()

if len(sys.argv) < 2:
	print "参数错误"
	exit(0)
else:
	daemon.daemon_exec(sys.argv[1])

logging.basicConfig(level=logging.INFO)
s = sockets.createSocket()
try:
	while True:
		try:
			conn, addr = s.accept()
			thread.start_new_thread(dealClient, (conn, addr))
		except:
			if conn is not None:
				conn.close()
except:
	s.close()
