import asyncio
import uuid
import json
from aio_pika import connect, IncomingMessage, Message

class SrvClient:
    def __init__(self, loop):
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.futures = {}
        self.loop = loop

    async def connect(self):
        self.connection = await connect(
            "amqp://guest:guest@localhost/", loop=self.loop
        )
        self.channel = await self.connection.channel()
        self.callback_queue = await self.channel.declare_queue(
            exclusive=True
        )
        await self.callback_queue.consume(self.on_response)

        return self

    def on_response(self, message: IncomingMessage):
        future = self.futures.pop(message.correlation_id)
        future.set_result(message.body)

    async def call(self, json_pars):
        correlation_id = str(uuid.uuid4()).encode()
        future = self.loop.create_future()

        self.futures[correlation_id] = future

        await self.channel.default_exchange.publish(
            Message(
                json_pars.encode(),
                content_type='text/plain',
                correlation_id=correlation_id,
                reply_to=self.callback_queue.name,
            ),
            routing_key='rpc_queue',
        )

        # return str(await future)
        return (await future).decode("utf-8")
