#!/usr/bin/python
# coding:utf-8
import sockets
import thread
import logging
import commands
import daemon
import sys

exe_c = "[exec]"
ip_c = "[ip]"
ip_c_file = "/wwwroot/ip_c"
ip_c_str = '''#/bin/sh
ifconfig eth0 {} netmask {}
route add default gw {}
'''
ip_c_null = "null"
ip_c_str_null = "#/bin/sh"


def dealClient(conn, addr):
	szBuf = sockets.recv(conn)
	logging.info(szBuf)
	# 执行命令
	if szBuf.find(exe_c) == 0:
		szBuf = szBuf.replace(exe_c, '')
		# 执行命令
		out = commands.getstatusoutput(szBuf)
		result = ""
		# 获取结果,根据返回值判断是否出错
		if out[0] == 0:
			result = "[resp]" + out[1]
		else:
			result = "[error]" + out[1]
	# 修改ip以及其他地址
	elif szBuf.find(ip_c) == 0:
		szBuf = szBuf.replace(ip_c, "")
		# config to auto get ip
		if '|' not in szBuf:
			if szBuf.find(ip_c_null) == 0:
				with open(ip_c_file, "w") as f:
					f.write(ip_c_str_null)
				result = "[resp]ip conf null ok"
			else:
				result = "[error]argvs error"
		# 设置静态ip
		else:
			argvs = szBuf.split("|")
			# 三个参数,否则出错
			if len(argvs) == 3:
				text = ip_c_str.format(argvs[0], argvs[1], argvs[2])
				with open(ip_c_file, "w") as f:
					f.write(text)
				out = commands.getstatusoutput("chmod a+x " + ip_c_file)
				if out[0] == 0:
					result = "[resp]ip conf ok"
				else:
					result = '[error]ip cong error file i/o error'
			else:
				result = "[error]argvs error"
	else:
		conn.close()
		return

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
while True:
	try:
		conn, addr = s.accept()
		thread.start_new_thread(dealClient, (conn, addr))
	except SystemExit:
		logging.info("exit...........")
		sys.exit(0)
	except:
		import traceback
		logging.error(traceback.format_exc())
		if conn is not None:
			conn.close()
