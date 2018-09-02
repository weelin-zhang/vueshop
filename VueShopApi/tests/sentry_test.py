# _*_ coding:utf-8 _*_

__author__ = 'weelin'
__date__ = '18/9/2下午12:57'

dsn = 'http://a8ce22bdb89c4989bdadc6fdf0a9dcc5@127.0.0.1:9000/2'



from raven import Client

client = Client(dsn)

try:
    a = {}
    del a
except ZeroDivisionError:
    client.captureException()