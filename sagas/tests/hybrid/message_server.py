import asyncio
from functools import partial
from aio_pika import connect, IncomingMessage, Exchange, Message
import hello_pb2

async def on_message(exchange: Exchange, message: IncomingMessage):
    with message.process():
        # n = int(message.body.decode())
        req=hello_pb2.ResponseHello()
        req.ParseFromString(message.body)
        # req=json.loads(message.body.decode())

        print(" [.] %s" % req)

        resp=hello_pb2.ResponseHello(response=req.response+"+world")
        # response = str(fib(n)).encode()
        response=resp.SerializeToString()

        await exchange.publish(
            Message(
                body=response,
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
    loop.create_task(main(loop, 'rpc_queue_2'))

    # we enter a never-ending loop that waits for data
    # and runs callbacks whenever necessary.
    print(" [x] Awaiting RPC requests")
    loop.run_forever()
