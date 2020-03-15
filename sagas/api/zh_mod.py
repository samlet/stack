from sanic import Blueprint
from sanic.response import json

zh = Blueprint('zh', url_prefix='/zh')


@zh.post("/hownet/<target>")
async def extract(request, target):
    """
    $ curl -d '{"word":"大学生"}' \
        -H "Content-Type: application/json" -X POST \
        localhost:1700/zh/hownet/sememes | json

    :param request:
    :return:
    """
    from sagas.zh.hownet_procs import hownet_procs

    rd = request.json
    fn_map={'sememes': lambda : hownet_procs.build_sememe_trees(rd['word']),
            }
    result=fn_map[target]() if target in fn_map else []
    return json(result)

