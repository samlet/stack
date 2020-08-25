'''
$ celery -A simple worker --loglevel=info
'''
import time

from celery import Celery
from sagas.cloud.app_sagas import app
# app = Celery('tasks', broker='pyamqp://guest@localhost//')
# app = Celery('tasks', backend='rpc://', broker='pyamqp://')

@app.task
def add(x, y):
    return x + y

@app.task
def mul(x, y):
    return x * y

@app.task
def xsum(numbers):
    return sum(numbers)
