import pickle
import redis

r = redis.StrictRedis('localhost')

def put_object(key, val):
    p_mydict = pickle.dumps(val)
    r.set(key,p_mydict)

def get_object(key):
    read_dict = r.get(key)
    val = pickle.loads(read_dict)
    return val
