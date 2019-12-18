from typing import Dict, Text, Any, List, Union

import pickle
import redis
import json
from sagas.conf.conf import cf

class Bucket(object):
    def __init__(self):
        self.r = redis.StrictRedis(cf.ensure('redis'))

    def put_object(self, key, val):
        p_mydict = pickle.dumps(val)
        self.r.set(key,p_mydict)

    def get_object(self, key):
        read_dict = self.r.get(key)
        val = pickle.loads(read_dict)
        return val

class JsonStore(object):
    def __init__(self):
        self.r = redis.Redis(cf.ensure('redis'))

    def put(self, name:Text, key:Text, val:Dict):
        self.r.hset(name, key, json.dumps(val, ensure_ascii=False))

    def get(self, name:Text, key:Text) -> Dict:
        response = self.r.hget(name, key)
        t = response.decode('utf8')
        return json.loads(t)

bucket=Bucket()
json_store=JsonStore()

