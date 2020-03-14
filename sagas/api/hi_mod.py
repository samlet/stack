from sanic import Blueprint
from sanic.response import json

hi = Blueprint('hi', url_prefix='/hi')


@hi.post("/iwn/<target>")
async def extract(request, target):
    """
    $ curl -d '{"word":"सेब", "pos":"noun"}' \
        -H "Content-Type: application/json" -X POST \
        localhost:1700/hi/iwn/hypers | json

    :param request:
    :return:
    """
    from sagas.hi.iwn_procs import iwn_procs

    rd = request.json
    word = rd['word']
    pos=rd['pos']
    fn_map={'hypers': iwn_procs.get_word_hypers,
            }
    result=fn_map[target](word, pos) if target in fn_map else []
    return json(result)

