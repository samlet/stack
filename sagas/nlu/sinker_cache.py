from typing import Text, Any, Dict, List, Union
from sagas.conf.conf import cf
from sagas.nlu.sinker_intf import SinkerStoreIntf

bucket_id=lambda h_id, user=None: f"{cf.user}:{h_id}" if user is None else f"{user}:{h_id}"
class CacheStore(SinkerStoreIntf):
    def __init__(self):
        import redis
        self.r=redis.StrictRedis(decode_responses=True)

    def store_all(self, hats:Dict[Text, Dict[Text, Any]], user=None):
        with self.r.pipeline() as pipe:
            for h_id, hat in hats.items():
                id=bucket_id(h_id, user)
                pipe.hmset(id, hat)
            pipe.execute()
        self.r.bgsave()

    def store(self, bucket:Text, values:Dict[Text, Any], user=None):
        self.r.hmset(bucket_id(bucket, user), values)

    def get_bucket(self, bucket:Text, user=None):
        return self.r.hgetall(bucket_id(bucket, user))

cache_store=CacheStore()

class CacheCli(object):
    def all_keys(self):
        return cache_store.r.keys()  # Careful on a big DB. keys() is O(N)

    def bucket(self, bucket, user=None):
        """
        Prepare:
            $ sj '新幹線で東京から大阪まで行きました。'
        Query:
            $ python -m sagas.nlu.sinker_cache bucket transport
        :param bucket:
        :param user:
        :return:
        """
        from pprint import pprint
        pprint(cache_store.get_bucket(bucket, user))

if __name__ == '__main__':
    import fire
    fire.Fire(CacheCli)

