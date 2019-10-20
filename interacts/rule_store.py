import redis

class RuleStore(object):
    def __init__(self):
        self.r = redis.Redis()
