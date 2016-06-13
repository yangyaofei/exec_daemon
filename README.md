# exec_daemon
用来执行shell命令的daemon

简单的守护进程,用以执行一些程序无法执行的命令.

如低权限cgi无法执行重启mysql服务,就可以用这个.

当然想安全,请加密

# 使用
server.py start|stop|restart

# daemon部分
使用了@clowwindy 的shadowsock中的daemon代码
