import redis
import random

class MapStore(object):
    def __init__(self):
        self.r = redis.Redis()
        random.seed(444)
        self.hats = {f"hat:{random.getrandbits(32)}": i for i in (
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
        self.keys=list(self.hats.keys())

        with self.r.pipeline() as pipe:
            for h_id, hat in self.hats.items():
                pipe.hmset(h_id, hat)
            pipe.execute()
        self.r.bgsave()

    def get_df(self):
        import sagas
        return sagas.dict_df(list(self.hats.values()))

    def get_record(self, id):
        # "hat:56854717"
        return self.r.hgetall(id)

    def modify(self):
        itemid=self.keys[0]
        self.r.hincrby(itemid, "quantity", -1)
        self.r.hset(itemid, 'color', b'blue')

map_store=MapStore()
