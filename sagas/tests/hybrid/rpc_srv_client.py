import asyncio
import uuid
import json
from aio_pika import connect, IncomingMessage, Message

from sagas.hybrid.srv_client import SrvClient

async def main(loop):
    rpc = await SrvClient(loop).connect()
    print(" [x] Requesting ...")
    json_pars = json.dumps({'_service': 'testScv',
                            'defaultValue': 5.5,
                            'message': "hello world"})
    response = await rpc.call(json_pars)
    print(" [.] Got %s" % response)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
