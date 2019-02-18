import asyncio
import traceback

from py4j.protocol import Py4JError
from aio_pika import connect_robust
from aio_pika.patterns import RPC
from sagas.ofbiz.entities import OfEntity as e, finder
from sagas.ofbiz.services import OfService as s, oc
import datetime
import logging
import json

logger = logging.getLogger(__name__)
# logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s',
#                      level=logging.INFO, stream=sys.stdout)

def error_routine(e):
    cause = (e.java_exception.getMessage())
    logging.error(cause)
    traceback.print_exc()
    # if e.cause is not None:
    #     print(e.cause)
    return json.dumps({'_result': 2,
                       'message': e.errmsg + cause,
                       'messages': str(e).splitlines()})

async def multiply(*, x, y):
    return x * y

async def notes(*, start, limit):
    logging.info("getting notes from %d with limit %d", start, limit)
    return e('json').listNoteData(_offset=start,_limit=limit)

async def entites(*, entity, start, limit):
    try:
        result = finder.find_list(entity, limit, start)
        ctx=oc.jmap(_result=0, data=result)
        # return oc.j.ValueHelper.valueListToJson(result)
        return oc.j.ValueHelper.mapToJson(ctx)
    except Py4JError as e:
        return error_routine(e)

async def echo(*, value, message):
    return json.dumps(dict(_result=0, value=value, message=message))

async def routines():
    connection = await connect_robust(
        "amqp://guest:guest@127.0.0.1/"
    )

    # Creating channel
    channel = await connection.channel()

    rpc = await RPC.create(channel)
    await rpc.register('multiply', multiply, auto_delete=True)
    await rpc.register('notes', notes, auto_delete=True)
    await rpc.register('entities', entites, auto_delete=True)
    await rpc.register('echo', echo, auto_delete=True)

    return connection


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(routines())

    print(".. routines serve.")
    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())
        loop.shutdown_asyncgens()
