from aiohttp import web
import textwrap
import asyncio
from aio_pika import connect_robust
from aio_pika.patterns import RPC

class HybridServ(object):
    async def intro(self, request):
        txt = textwrap.dedent("""\
            Type {url}/hello/John  {url}/simple or {url}/change_body
            in browser url bar
        """).format(url='127.0.0.1:8080')
        binary = txt.encode('utf8')
        resp = web.StreamResponse()
        resp.content_length = len(binary)
        resp.content_type = 'text/plain'
        await resp.prepare(request)
        await resp.write(binary)
        return resp

    async def simple(self, request):
        return web.Response(text="Simple answer")

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

    async def main(self, request):
        if not self.connected:
            self.connection = await connect_robust(
                "amqp://guest:guest@127.0.0.1/"
            )

            # Creating channel
            self.channel = await self.connection.channel()
            self.rpc = await RPC.create(self.channel)
            self.connected=True

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

    def init(self):
        self.connected=False

        app = web.Application()
        app.router.add_get('/', self.intro)
        app.router.add_get('/simple', self.simple)
        app.router.add_get('/hello/{name}', self.hello)
        app.router.add_get('/hello', self.hello)
        app.router.add_get('/main/{count}', self.main)
        return app

if __name__ == '__main__':
    serv=HybridServ()
    web.run_app(serv.init())

