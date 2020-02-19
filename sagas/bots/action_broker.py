import asyncio
import logging
from functools import partial
from aio_pika import connect, IncomingMessage, Exchange, Message
from blueprints_pb2 import BlueInteract, BotMessage
from sagas.bots.action_runner import ActionRunner
from values_pb2 import TaJson
import json
import sys

from google.protobuf.json_format import MessageToJson
from client_wrapper import ServiceClient

import nlpserv_pb2 as nlp_messages
import nlpserv_pb2_grpc as nlp_service
from sagas.misc.utils import dump

logging.getLogger('pika').setLevel(logging.INFO)
logging.getLogger('aio_pika').setLevel(logging.INFO)

class ActionBroker(object):
    def __init__(self):
        self.runner= ActionRunner()

    async def handle(self, req: BlueInteract):
        cnt=BotMessage()
        cnt.ParseFromString(req.body)
        result=self.runner.execute(req.uri, cnt.message)

        resp = TaJson(content=json.dumps(result, indent=2, ensure_ascii=False))
        response = resp.SerializeToString()
        return response

class HanlpDelegator(object):
    def __init__(self):
        self.client=ServiceClient(nlp_service, 'NlpProcsStub', 'localhost', 10052)

    async def handle(self, req: BlueInteract):
        cnt=BotMessage()
        cnt.ParseFromString(req.body)
        result=self.extract(cnt.message)
        response = result.SerializeToString()
        return response

    def tokenize(self, text):
        request = nlp_messages.NlTokenizerRequest(text=nlp_messages.NlText(text=text))
        response = self.client.Tokenizer(request)
        return response

    def extract(self, text):
        request = nlp_messages.NlTokenizerRequest(text=nlp_messages.NlText(text=text))
        response = self.client.EntityExtractor(request)
        return response

action_broker=ActionBroker()
hanlp=HanlpDelegator()

async def on_message(exchange: Exchange, message: IncomingMessage):
    with message.process():
        # n = int(message.body.decode())
        req=BlueInteract()
        req.ParseFromString(message.body)
        # req=json.loads(message.body.decode())

        print(" [.] %s - %s" % (req.uri, req.type))
        if req.type=="nlp":
            resp = await hanlp.handle(req)
        else:
            resp = await action_broker.handle(req)

        await exchange.publish(
            Message(
                body=resp,
                correlation_id=message.correlation_id
            ),
            routing_key=message.reply_to
        )
        print('Request complete')


async def main(loop, queue_name):
    # Perform connection
    connection = await connect(
        "amqp://guest:guest@localhost/", loop=loop
    )

    # Creating a channel
    channel = await connection.channel()

    # Declaring queue
    queue = await channel.declare_queue(queue_name)

    # Start listening the queue with name 'hello'
    await queue.consume(
        partial(
            on_message,
            channel.default_exchange
        )
    )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop, 'rpc_ai'))

    # we enter a never-ending loop that waits for data
    # and runs callbacks whenever necessary.
    print(" [x] Awaiting ai interact requests")
    loop.run_forever()
