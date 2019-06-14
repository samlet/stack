import datetime
from dateutil.parser import parse

def now():
    return datetime.datetime.now().isoformat()

def now_jdbc():
    return datetime.datetime.now().isoformat(' ')

def to_jdbc(dt):
    return parse(dt).isoformat(' ')

