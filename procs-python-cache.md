# procs-python-cache.md
⊕ [Speed up your code by using a cache in Python | The Python Corner](https://www.thepythoncorner.com/2018/04/how-to-make-your-code-faster-by-using-a-cache-in-python/?source=post_page-----fb169fbcbb0b----------------------)
⊕ [cachetools · PyPI](https://pypi.org/project/cachetools/)
    ⊕ [cachetools — Extensible memoizing collections and decorators — cachetools 4.0.0 documentation](https://cachetools.readthedocs.io/en/stable/)

## start
```sh
pip install cachetools
```

```python
import time
import datetime

from cachetools import cached, TTLCache  # 1 - let's import the "cached" decorator and the "TTLCache" object from cachetools
cache = TTLCache(maxsize=100, ttl=300)  # 2 - let's create the cache object.

@cached(cache)  # 3 - it's time to decorate the method to use our cache system!
def get_candy_price(candy_id):
    # let's use a sleep to simulate the time your function spends trying to connect to
    # the web service, 5 seconds will be enough.
    time.sleep(5)

    # let's pretend that the price returned by the web service is $1 for candies with a
    # odd candy_id and $1,5 for candies with a even candy_id

    price = 1.5 if candy_id % 2 == 0 else 1

    return (datetime.datetime.now().strftime("%c"), price)


# now, let's simulate 20 customers in your show.
# They are asking for candy with id 2 and candy with id 3...
for i in range(0,20):
    print(get_candy_price(2))
    print(get_candy_price(3))
```

+ sagas/nlu/words_servant.py

```python
from cachetools import cached, TTLCache
cache = TTLCache(maxsize=100, ttl=300)

@cached(cache)
def get_synsets_as_json(lang, word, pos):
    from sagas.nlu.omw_extended import get_synsets
    sets = get_synsets(lang, word, pos)
    r = [c.name() for c in sets]
    data_y = json.dumps(r)
    return data_y

@app.route('/get_synsets', methods = ['POST'])
def handle_get_synsets():
    content = request.get_json()
    word = content['word']
    ...
    return get_synsets_as_json(lang, word, pos)    
```

```python
from cachetools import cached, LRUCache, TTLCache

# speed up calculating Fibonacci numbers with dynamic programming
@cached(cache={})
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

# cache least recently used Python Enhancement Proposals
@cached(cache=LRUCache(maxsize=32))
def get_pep(num):
    url = 'http://www.python.org/dev/peps/pep-%04d/' % num
    with urllib.request.urlopen(url) as s:
        return s.read()

# cache weather data for no longer than ten minutes
@cached(cache=TTLCache(maxsize=1024, ttl=600))
def get_weather(place):
    return owm.weather_at_place(place).get_weather()
```

## cachedmethod
⊕ [cachetools — Extensible memoizing collections and decorators — cachetools 4.0.0 documentation](https://cachetools.readthedocs.io/en/stable/#cachetools.cachedmethod)

Decorator to wrap a class or instance method with a memoizing callable that saves results in a (possibly shared) cache.

The main difference between this and the cached() function decorator is that cache and lock are not passed objects, but functions. Both will be called with self (or cls for class methods) as their sole argument to retrieve the cache or lock object for the method’s respective instance or class.

Note

As with cached(), the context manager obtained by calling lock(self) will only guard access to the cache itself. It is the user’s responsibility to handle concurrent calls to the underlying wrapped method in a multithreaded environment.

One advantage of cachedmethod() over the cached() function decorator is that cache properties such as maxsize can be set at runtime:

```python
class CachedPEPs(object):

    def __init__(self, cachesize):
        self.cache = LRUCache(maxsize=cachesize)

    @cachedmethod(operator.attrgetter('cache'))
    def get(self, num):
        """Retrieve text of a Python Enhancement Proposal"""
        url = 'http://www.python.org/dev/peps/pep-%04d/' % num
        with urllib.request.urlopen(url) as s:
            return s.read()

peps = CachedPEPs(cachesize=10)
print("PEP #1: %s" % peps.get(1))
```

When using a shared cache for multiple methods, be aware that different cache keys must be created for each method even when function arguments are the same, just as with the @cached decorator:

```python
class CachedReferences(object):

    def __init__(self, cachesize):
        self.cache = LRUCache(maxsize=cachesize)

    @cachedmethod(lambda self: self.cache, key=partial(hashkey, 'pep'))
    def get_pep(self, num):
        """Retrieve text of a Python Enhancement Proposal"""
        url = 'http://www.python.org/dev/peps/pep-%04d/' % num
        with urllib.request.urlopen(url) as s:
            return s.read()

    @cachedmethod(lambda self: self.cache, key=partial(hashkey, 'rfc'))
    def get_rfc(self, num):
        """Retrieve text of an IETF Request for Comments"""
        url = 'https://tools.ietf.org/rfc/rfc%d.txt' % num
        with urllib.request.urlopen(url) as s:
            return s.read()

docs = CachedReferences(cachesize=100)
print("PEP #1: %s" % docs.get_pep(1))
print("RFC #1: %s" % docs.get_rfc(1))
```

