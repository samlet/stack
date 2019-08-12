from flask import Flask
from flask import request
import logging
logger = logging.getLogger('servant')

app = Flask(__name__)

@app.route("/")
def home():
    return "servant: multilang"

@app.route('/entities', methods = ['POST'])
def handle_entities():
    from sagas.nlu.net_context import EntitiesRequest
    from sagas.nlu.extractor_natasha import ru_natasha

    ctx=EntitiesRequest(request.get_json())
    exts={'ru':lambda ctx: ru_natasha.extract(ctx.sents),
          }
    if ctx.lang not in exts:
        logger.error("Cannot support language %s", ctx.lang)
        return ctx.empty_set()
    else:
        return ctx.wrap_result(exts[ctx.lang](ctx))

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=8091, debug=True)
    app.run(host='0.0.0.0', port=8095)

