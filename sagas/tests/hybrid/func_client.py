import asyncio
from functools import partial
from aio_pika import connect, IncomingMessage, Exchange, Message
from aio_pika.patterns.rpc import RPC, log as rpc_logger

from sagas.tests.hybrid.func_server import FuncBase

loop = asyncio.get_event_loop()

class FuncClient(FuncBase):
    async def invoke(self):
        channel = await self.create_channel()
        rpc= await RPC.create(channel, auto_delete=True)
        result = await rpc.proxy.test.rpc(foo=None, bar=None)
        print(result)

        await rpc.close()

if __name__ == '__main__':
    c=FuncClient()
    loop.run_until_complete(c.invoke())


