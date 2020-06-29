from sanic import Sanic
from sanic.response import json
from sanic import Blueprint

from sagas.listings.listings_cli import ListingsCli, listings

bp = Blueprint('root_blueprint')

@bp.route('/')
async def bp_root(request):
    return json({'mod': 'listings'})

@bp.post("/proc/<target>/<item>")
async def proc(request, target, item):
    """
    $ curl -s -d '{"sentence":"Hugging Face is a technology company based in New York and Paris"}' \
        -H "Content-Type: application/json" -X POST \
        localhost:1755/proc/t5/T5_de | json
    $ curl -s -d '{"sentence":"Hugging Face is a technology company"}' \
        -H "Content-Type: application/json" -X POST \
        localhost:1755/proc/simple/Simple | json

    :param request:
    :return:
    """
    from mode.utils.compat import want_bytes, want_str
    rd = request.json
    result=listings.proc(target, item, rd)
    return json(result, dumps=lambda c: want_str(c.dumps(serializer='json')))

app = Sanic(__name__)
app.blueprint(bp)

class ListingsServant(object):
    def run(self, port=1755, debug=True):
        """
        $ python -m sagas.listings.listings_servant run 1755 False
        $ curl localhost:1755
        """
        app.run(host='0.0.0.0', port=port, debug=debug)

if __name__ == '__main__':
    import fire
    fire.Fire(ListingsServant)



