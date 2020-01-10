import time

from sagas.ofbiz.blackboard import *
import sys
import asyncio
from aio_pika import connect, Message, DeliveryMode, ExchangeType

class Sender(object):
    async def send(self, loop):
        # Perform connection
        connection = await connect(
            "amqp://guest:guest@localhost/",
            # "amqp://guest:guest@192.168.0.101/",
            loop=loop
        )

        # Creating a channel
        channel = await connection.channel()

        topic_logs_exchange = await channel.declare_exchange(
            'topic_logs', ExchangeType.TOPIC
        )

        routing_key = (
            sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
        )

        message_body = (
            b' '.join(arg.encode() for arg in sys.argv[2:])
            or
            b"Hello World!"
        )

        message = Message(
            message_body,
            delivery_mode=DeliveryMode.PERSISTENT
        )

        # Sending the message
        await topic_logs_exchange.publish(
            message, routing_key=routing_key
        )

        print(" [x] Sent %r" % message)

        await connection.close()

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

async def send_main(loop):
    print('hello')
    ss = Sender()
    # loop.run_forever()
    await ss.send(loop)
    await asyncio.sleep(1)
    print('world')

if __name__ == '__main__':
    import asyncio
    from sagas.tests.bus.aio.receive_logs_topic import main

    # message receiver
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))

    # we enter a never-ending loop that waits for
    # data and runs callbacks whenever necessary.
    print(" [*] Waiting for messages ..")

    # bbs=Blackboard()
    # bbs.send('hello')
    # asyncio.run_coroutine_threadsafe(send_main(loop), loop)
    #
    # # loop.run_until_complete()
    # try:
    #     while True:
    #         time.sleep(_ONE_DAY_IN_SECONDS)
    # except KeyboardInterrupt:
    #     pass


