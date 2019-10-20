import json

import redis
import random

class JsonStore(object):
    def __init__(self):
        self.r = redis.Redis()

        random.seed(444)
        hats = {f"hat:{random.getrandbits(32)}": i for i in (
            {
                "color": "black",
                "price": 49.99,
                "style": "fitted",
                "quantity": 1000,
                "npurchased": 0,
            },
            {
                "color": "maroon",
                "price": 59.99,
                "style": "hipster",
                "quantity": 500,
                "npurchased": 0,
            },
            {
                "color": "green",
                "price": 99.99,
                "style": "baseball",
                "quantity": 200,
                "npurchased": 0,
            })
                }

        self.init_store(hats)

    def init_store(self,hats):
        self.keys = list(hats.keys())
        with self.r.pipeline() as pipe:
            for h_id, hat in hats.items():
                # pipe.hmset(h_id, hat)
                pipe.hset(h_id, 'cnt', json.dumps(hat, ensure_ascii=False))
            pipe.execute()
        self.r.bgsave()

    def get_df(self):
        import sagas
        hats={}
        for key in self.keys:
            response = self.r.hget(key, 'cnt')
            t = response.decode('utf8')
            hats[key]=json.loads(t)
        return sagas.dict_df(list(hats.values()))

    def get_record(self, id):
        # "hat:56854717"
        return self.r.hgetall(id)

    def modify(self):
        itemid=self.keys[0]
        x={
            "color": "green",
            "price": random.getrandbits(8),
            "style": "baseball(upd)",
            "quantity": 200,
            "npurchased": 0,
        }
        self.r.hset(itemid, 'cnt', json.dumps(x, ensure_ascii=False))

    def add(self):
        itemid=f"hat:{random.getrandbits(32)}"
        self.keys.append(itemid)
        x = {
            "color": "black",
            "price": random.getrandbits(8),
            "style": "baseball(upd)",
            "quantity": 200,
            "npurchased": 0,
        }
        self.r.hset(itemid, 'cnt', json.dumps(x, ensure_ascii=False))

    def clear(self):
        for k in self.keys:
            self.r.hdel(k, 'cnt')

        self.keys=[]
        self.init_store(hats = {f"hat:{random.getrandbits(32)}": i for i in (
            {
                "color": "black",
                "price": 49.99,
                "style": "fitted",
                "quantity": 1000,
                "npurchased": 0,
            },)})

json_store=JsonStore()

