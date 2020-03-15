from sanic import Blueprint
from sanic.response import json

hi = Blueprint('hi', url_prefix='/hi')


@hi.post("/iwn/<target>")
async def extract(request, target):
    """
    $ curl -d '{"word":"सेब", "pos":"noun"}' \
        -H "Content-Type: application/json" -X POST \
        localhost:1700/hi/iwn/hypers | json
    $ curl -d '{"word":"nonexistent", "pos":"noun"}' \
        -H "Content-Type: application/json" -X POST \
        localhost:1700/hi/iwn/hypers | json
    $ curl -d '{"id":8358, "pos":"noun"}' \
        -H "Content-Type: application/json" -X POST \
        localhost:1700/hi/iwn/hypers_by_id | json

    :param request:
    :return:
    """
    from sagas.hi.iwn_procs import iwn_procs

    rd = request.json
    pos=rd['pos']
    fn_map={'hypers': lambda : iwn_procs.get_word_hypers(rd['word'], pos),
            'hypers_by_id': lambda : iwn_procs.get_hypers_by_id(rd['id'], pos),
            }
    result=fn_map[target]() if target in fn_map else []
    return json(result)

