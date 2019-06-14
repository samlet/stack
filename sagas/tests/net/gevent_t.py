import gevent
from gevent import socket

"""
⊕ [简介 - gevent 1.4.1.dev0文档](http://www.gevent.org/intro.html)

生成作业后，gevent.joinall()等待它们完成，最多允许2秒钟。
然后通过检查value财产收集结果。该gevent.socket.gethostbyname()函数具有与标准相同的接口，
socket.gethostbyname()但它不会阻止整个解释器，因此让其他greenlet不受阻碍地继续其请求。
"""
urls = ['www.google.com', 'www.example.com', 'www.python.org']
jobs = [gevent.spawn(socket.gethostbyname, url) for url in urls]
gevent.joinall(jobs, timeout=2)
print([job.value for job in jobs])

