from typing import Text, Dict, List

from cachetools import cached
from flask import Flask
from flask import request, Blueprint
import logging
import json

logger = logging.getLogger(__name__)

# app = Flask(__name__)
multilang=Blueprint('multilang', __name__)

# @multilang.route("/")
# def home():
#     return "servant: multilang"

@cached(cache={})
def extract_ru(sents:Text):
    from sagas.nlu.extractor_natasha import ru_natasha
    return ru_natasha.extract(sents)

@multilang.route('/entities', methods = ['POST'])
def handle_entities():
    from sagas.nlu.net_context import EntitiesRequest

    ctx=EntitiesRequest(request.get_json())
    exts={'ru':lambda ctx: extract_ru(ctx.sents),
          }
    if ctx.lang not in exts:
        logger.error("Cannot support language %s", ctx.lang)
        return ctx.empty_set()
    else:
        return ctx.wrap_result(exts[ctx.lang](ctx))

def tokens_zh(s):
    from sagas.zh.ltp_procs import ltp
    return ltp.tokens(s)

def tokens_ja(s):
    from sagas.ja.knp_helper import tokens
    return tokens(s)

@cached(cache={})
def sent_tokens(sents, lang):
    logger.debug(f"tokens {lang}: {sents}")
    fn_map={'zh': lambda s: tokens_zh(s),
            'ja': lambda s: tokens_ja(s),
            }
    if lang in fn_map:
        rs= fn_map[lang](sents)
    else:
        rs= sents.split(' ')
    logger.debug(f"tokens {lang} result: {rs}")
    return json.dumps(rs)

@multilang.route('/tokens', methods = ['POST'])
def handle_tokens():
    content = request.get_json()
    return sent_tokens(content['sents'], content['lang'])

# if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=8091, debug=True)
    # app.run(host='0.0.0.0', port=8095)

