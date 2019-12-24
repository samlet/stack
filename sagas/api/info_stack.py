from sanic import Sanic

from .ner_mod import ner_mod
from .root_mod import bp
from .info_mod import info

app = Sanic(__name__)
app.blueprint(bp)
app.blueprint(info)
app.blueprint(ner_mod)

"""
$ python -m sagas.api.info_stack
$ curl localhost:1700
"""
app.run(host='0.0.0.0', port=1700, debug=True)


