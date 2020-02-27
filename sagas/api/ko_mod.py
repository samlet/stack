from sanic import Blueprint
from sanic.response import json

ko = Blueprint('ko', url_prefix='/ko')


@ko.post("/extract/<target>")
async def extract(request, target):
    """
    $ curl -d '{"sents":"피자와 스파게티가"}' \
        -H "Content-Type: application/json" -X POST \
        localhost:1700/ko/extract/pos | json

    :param request:
    :return:
    """
    from sagas.ko.ko_helper import ko_helper

    rd = request.json
    sents = rd['sents']
    fn_map={'nouns': ko_helper.nouns,
            'pos': ko_helper.pos,
            }
    result=fn_map[target](sents) if target in fn_map else []
    return json(result)

