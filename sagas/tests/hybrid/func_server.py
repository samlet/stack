import asyncio
from functools import partial
from aio_pika import connect, IncomingMessage, Exchange, Message
from aio_pika import Connection, connect, Channel, Queue, Exchange
from aio_pika.patterns.rpc import RPC, log as rpc_logger
import logging
import os
from yarl import URL

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


AMQP_URL = URL(os.getenv("AMQP_URL", "amqp://guest:guest@localhost"))

if not AMQP_URL.path:
    AMQP_URL.path = '/'

def rpc_func(*, foo, bar):
    assert not foo
    assert not bar

    return {'foo': 'bar'}

class FuncBase(object):
    def __init__(self, loop):
        self._cleanups = []
        # self.loop = asyncio.get_event_loop()
        self.loop = loop

    def addCleanup(self, function, *args, **kwargs):
        """Add a function, with arguments, to be called when the test is
        completed. Functions added are called on a LIFO basis and are
        called after tearDown on test failure or success.

        Cleanup items are called even if setUp fails (unlike tearDown)."""
        self._cleanups.append((function, args, kwargs))

    async def create_connection(self, cleanup=True) -> Connection:
        client = await connect(str(AMQP_URL), loop=self.loop)

        if cleanup:
            self.addCleanup(client.close)

        return client

    async def create_channel(self, connection=None,
                             cleanup=True, **kwargs) -> Channel:
        if connection is None:
            connection = await self.create_connection()

        channel = await connection.channel(**kwargs)

        if cleanup:
            self.addCleanup(channel.close)

        return channel

    async def declare_queue(self, *args, **kwargs) -> Queue:
        if 'channel' not in kwargs:
            channel = await self.create_channel()
        else:
            channel = kwargs.pop('channel')

        queue = await channel.declare_queue(*args, **kwargs)
        self.addCleanup(queue.delete)
        return queue

    async def declare_exchange(self, *args, **kwargs) -> Exchange:
        if 'channel' not in kwargs:
            channel = await self.create_channel()
        else:
            channel = kwargs.pop('channel')

        exchange = await channel.declare_exchange(*args, **kwargs)
        self.addCleanup(exchange.delete)
        return exchange

class Funcs(FuncBase):

    async def start(self):
        channel = await self.create_channel()
        self.rpc = await RPC.create(channel, auto_delete=True)

        await self.rpc.register('test.rpc', rpc_func, auto_delete=True)

    async def stop(self):
        await self.rpc.unregister(rpc_func)
        await self.rpc.close()

        # Close already closed
        await self.rpc.close()

async def main(loop):
    f=Funcs(loop)
    await f.start()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))

    # we enter a never-ending loop that waits for data
    # and runs callbacks whenever necessary.
    print(" [x] Awaiting RPC requests")
    loop.run_forever()
