from sanic import Blueprint
from sanic.response import json

info = Blueprint('info', url_prefix='/info')

@info.route("/ping")
async def ping(request):
    """
    $ curl localhost:1700/info/ping
    :param request:
    :return:
    """
    return json({ "hello": "world" })

@info.route('/env/<tag>')
async def env_handler(request, tag):
    """
    $ curl localhost:1700/info/env/PATH
    :param request:
    :param tag:
    :return:
    """
    import os
    return json({tag: os.environ.get(tag)})

@info.post('/echo/<tag>')
async def echo(request, tag):
    """
    $ curl -d '{"key1":"value1", "key2":"value2"}' \
        -H "Content-Type: application/json" -X POST \
        localhost:1700/info/echo/hi | json
    :param request:
    :param tag:
    :return:
    """
    data=request.json
    print("..", data)
    return json({tag:'POST request - {}'.format(request.json),
                 'keys': list(data.keys()),
                 })

