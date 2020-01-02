from sanic import Sanic

from .intents_mod import intents_mod
from .ner_mod import ner_mod
from .root_mod import bp
from .info_mod import info

app = Sanic(__name__)
app.blueprint(bp)
app.blueprint(info)
app.blueprint(ner_mod)
app.blueprint(intents_mod)

class InfoStack(object):
    def run(self, port=1700, debug=True):
        """
        $ python -m sagas.api.info_stack run 1700 False
        $ curl localhost:1700
        """
        app.run(host='0.0.0.0', port=1700, debug=debug)

if __name__ == '__main__':
    import fire
    fire.Fire(InfoStack)


