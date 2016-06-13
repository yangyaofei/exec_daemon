# coding:utf-8
import socket
BUFF_SIZE = 1024
SOCKET_PORT = 666


def createSocket():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(("localhost", SOCKET_PORT))
	s.listen(5)
	return s


def connectServer():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('localhost', SOCKET_PORT))
	return s


def recv(sock):
	szBuf = ''
	while(True):
		buf = sock.recv(BUFF_SIZE)
		szBuf += buf
		if(len(buf) < BUFF_SIZE):
			break
	return szBuf
