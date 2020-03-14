from sanic import Blueprint
from sanic.response import json

en = Blueprint('en', url_prefix='/en')


@en.post("/wsd/<target>")
async def extract_wsd(request, target):
    """
    $ curl -d '{"sents":"The sheet is twenty centimeters."}' \
        -H "Content-Type: application/json" -X POST \
        localhost:1700/en/wsd/default | json

    :param request:
    :return:
    """
    from pywsd import disambiguate
    from pywsd.similarity import max_similarity as maxsim
    from pywsd.lesk import simple_lesk

    rd = request.json
    sents = rd['sents']

    extract_syn=lambda r: (r[0], r[1].name(), r[1].definition())
    def extract_sents():
        rs = disambiguate(sents)
        return [extract_syn(r) for r in rs if r[1]]

    fn_map={'default': lambda: extract_sents(),
            'maxsim': lambda: [extract_syn(r) for r in disambiguate(
                sents, algorithm=maxsim,
                similarity_option='wup',
                keepLemmas=False) if r[1]],
            'lesk': lambda: simple_lesk(sents, rd['word']),
            }
    result=fn_map[target]() if target in fn_map else []
    return json(result)

