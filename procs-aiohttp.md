# procs-aiohttp.md
⊕ [how-to retrieve the data (body) in aiohttp server from requests.get · Issue #1155 · aio-libs/aiohttp](https://github.com/aio-libs/aiohttp/issues/1155)

+ `data` is `<MultiDictProxy()>` for which i didn't find much info
    It's https://multidict.readthedocs.io/en/stable/multidict.html#multidict.MultiDictProxy

+ In your case you might use `await request.json()`.

```python
def api_bgp_show_route(request):
      data = await request.post()
      assert data == {'topo':"switzerland", 'pop':"zrh", 'prefix':"1.1.1.1/32"}
```

⊕ [python - Query parameters of the get URL using aiohttp from python3.5 - Stack Overflow](https://stackoverflow.com/questions/47851096/query-parameters-of-the-get-url-using-aiohttp-from-python3-5)

```python
from aiohttp import web

async def method(request):
    ## here how to get query parameters
    param1 = request.rel_url.query['name']
    param2 = request.rel_url.query['age']
    result = "name: {}, age: {}".format(param1, param2)
    return web.Response(text=str(result))


if __name__ == '__main__':
    app = web.Application()
    app.router.add_route('GET', "/sample", method)

    web.run_app(app,host='localhost', port=11111)
# then you can try: http://localhost:11111/sample?name=xyz&age=xy and it is working.
```

