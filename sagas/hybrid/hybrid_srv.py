from aiohttp import web
import textwrap
import asyncio
from aio_pika import connect_robust
from aio_pika.patterns import RPC
import functools
import json

from sagas.hybrid.srv_client import SrvClient
import logging

logger = logging.getLogger(__name__)

class HybridServ(object):
    async def intro(self, request):
        txt = textwrap.dedent("""\
            Type {url}/hello/John  {url}/simple or {url}/change_body
            in browser url bar
        """).format(url='127.0.0.1:8099')
        binary = txt.encode('utf8')
        resp = web.StreamResponse()
        resp.content_length = len(binary)
        resp.content_type = 'text/plain'
        await resp.prepare(request)
        await resp.write(binary)
        return resp

    async def simple(self, request):
        """
        GET - http://localhost:8099/simple?name=xyz&age=xy
        :param request:
        :return:
        """
        # print(dict(request.GET))
        param1 = request.rel_url.query['name']
        param2 = request.rel_url.query['age']
        result = "name: {}, age: {}".format(param1, param2)
        return web.Response(text=result)

    async def hello(self, request):
        resp = web.StreamResponse()
        name = request.match_info.get('name', 'Anonymous')
        answer = ('Hello, ' + name).encode('utf8')
        resp.content_length = len(answer)
        resp.content_type = 'text/plain'
        await resp.prepare(request)
        await resp.write(answer)
        await resp.write_eof()
        return resp

    async def check_connect(self):
        if not self.connected:
            self.connection = await connect_robust(
                "amqp://guest:guest@127.0.0.1/", loop=self.loop
            )

            # Creating channel
            self.channel = await self.connection.channel()
            self.rpc = await RPC.create(self.channel)
            self.srv_client=await SrvClient(self.loop).connect()
            self.connected=True

    async def multiply(self, request):
        await self.check_connect()

        resp = web.StreamResponse()
        count = request.match_info.get('count', 5)
        print("count is {}".format(count))

        # Creates tasks by proxy object
        result=(await self.rpc.proxy.multiply(x=100, y=int(count)))

        answer = ('result: ' + str(result)).encode('utf8')
        resp.content_length = len(answer)
        resp.content_type = 'text/plain'
        await resp.prepare(request)
        await resp.write(answer)
        await resp.write_eof()
        return resp

    async def list_notes(self, request):
        """
        GET - http://localhost:8099/list_notes/0/10
        :param request:
        :return:
        """
        await self.check_connect()

        start = request.match_info.get('start', 0)
        limit= request.match_info.get('limit', 10)
        print("start {}, limit {}".format(start,limit))
        result = (await self.rpc.proxy.notes(start=int(start), limit=int(limit)))
        # await self.send_text(request, resp, result)

        return web.Response(text=result, status=200, content_type='application/json')

    async def list_entities(self, request):
        """
        GET - http://localhost:8099/list_entities/NoteData?_start=0&_limit=10
        :param request:
        :return:
        """
        await self.check_connect()

        entity=request.match_info.get('entity', '')
        start=0
        limit=10
        if 'start' in request.rel_url.query:
            start = request.rel_url.query['_start']
        if 'limit' in request.rel_url.query:
            limit = request.rel_url.query['_limit']

        logging.info("list {} start {}, limit {}".format(entity, start,limit))
        result = (await self.rpc.proxy.entities(entity=entity,
                                                start=int(start),
                                                limit=int(limit)))
        # await self.send_text(request, resp, result)

        return web.Response(text=result, status=200, content_type='application/json')

    # async def send_text(self, request, resp, answer):
    #     # resp = web.StreamResponse()
    #     resp.content_length = len(answer)
    #     resp.content_type = 'text/json'
    #     await resp.prepare(request)
    #     await resp.write(answer)
    #     await resp.write_eof()

    async def post(self, request):
        """
        POST - http://localhost:8099/post/path
        body(json) - {"x":5}
        :param request:
        :return:
        """
        # data = await request.post()
        data = await request.json()
        info=request.match_info.get('info', '_')
        print(data, type(data))
        return web.json_response({
            'method': 'post',
            'info': info,
            # 'args': dict(request.GET),
            'data': dict(data),
            'headers': dict(request.headers),
        }, dumps=functools.partial(json.dumps, indent=4))

    async def srv(self, request):
        """
        POST - http://localhost:8099/srv/testScv
        body(json) - {"defaultValue": 5.5, "message": "hello world"}
        :param request:
        :return:
        """
        await self.check_connect()

        req=await request.json()
        info = request.match_info.get('info', '')
        req['_service']=info
        print(info, '-', req)
        json_pars = json.dumps(req)
        result = await self.srv_client.call(json_pars)
        # print(" [.] Got %s" % response)
        # return await self.send_text(request, result)
        return web.Response(text=result, status=200, content_type='application/json')

    async def rpc(self, request):
        """
        POST - http://localhost:8099/rpc/echo
        body(json) - {"value": 5.5, "message": "hello world"}
        :param request:
        :return:
        """
        await self.check_connect()

        req=await request.json()
        info = request.match_info.get('info', '')
        print(info, '-', req)
        result=await self.rpc.call(info, kwargs=req)

        return web.Response(text=result, status=200, content_type='application/json')

    def init(self, loop):
        self.connected=False
        self.loop=loop
        self.srv_client=None

        app = web.Application()
        app.router.add_get('/', self.intro)
        app.router.add_get('/simple', self.simple)
        app.router.add_get('/hello/{name}', self.hello)
        app.router.add_get('/hello', self.hello)
        app.router.add_get('/multiply/{count}', self.multiply)
        app.router.add_post('/post/{info}', self.post)
        app.router.add_post('/srv/{info}', self.srv)
        app.router.add_post('/rpc/{info}', self.rpc)
        app.router.add_get('/list_notes/{start}/{limit}', self.list_notes)
        app.router.add_get('/list_entities/{entity}', self.list_entities)

        return app

if __name__ == '__main__':
    serv=HybridServ()
    v_loop = asyncio.get_event_loop()
    v_loop.set_debug(True)
    web.run_app(serv.init(v_loop), port=8099)

