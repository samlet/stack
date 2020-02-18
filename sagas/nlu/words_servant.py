from flask import Flask
from flask import request
import json
from sagas.nlu.wordnet_procs import WordNetProcs, predicate_chain, get_chains
from cachetools import cached, TTLCache
import logging
logger = logging.getLogger('servant')

# cache = TTLCache(maxsize=100, ttl=300)
app = Flask(__name__)

@app.route("/")
def home():
    return "servant: words"

@cached(cache={})
def predicate_word(word, lang, pos, kind, only_first):
    procs = WordNetProcs()
    r = procs.predicate(word, kind, lang=lang,
                        pos=None if pos=='*' else pos,
                        only_first=only_first)
    data_y = json.dumps({'result': r})
    return data_y

@app.route('/predicate', methods = ['POST'])
def handle_predicate():
    """
    检测synsets的lemma, 较宽泛, 不适用于rulesets
    :return:
    """
    content = request.get_json()
    return predicate_word(content['word'], content['lang'],
                          content['pos'],
                          content['kind'],
                          content['only_first']
                          )

@cached(cache={})
def predicate_chain_as_json(word,kind,lang,pos):
    r, c = predicate_chain(word, kind, lang=lang, pos=pos)
    data_y = json.dumps({'result': r, 'data': c})
    return data_y

@app.route('/predicate_chain', methods = ['POST'])
def handle_predicate_chain():
    """
    检测synsets的name, 更为严格
    :return:
    """
    content = request.get_json()
    word = content['word']
    lang = content['lang']
    pos=content['pos']
    if pos=='*':
        pos=None
    kind=content['kind']

    # r,c=predicate_chain(word, kind, lang=lang, pos=pos)
    # data_y = json.dumps({'result':r, 'data':c})
    return predicate_chain_as_json(word, kind, lang=lang, pos=pos)

@cached(cache={})
def get_chains_as_json(lang, raw_word, pos):
    word_parts = raw_word.split('/')  # 允许用'membaca/menbaca'形式
    try:
        for word in word_parts:
            r = get_chains(word, lang=lang, pos=pos)
            if len(r) > 0:
                data_y = json.dumps(r)
                return data_y
    except Exception as e:
        logger.error(
            "Failed to get chains for '{}'. "
            "Error: {}".format(raw_word, e))
    return '[]'

@app.route('/get_chains', methods = ['POST'])
def handle_get_chains():
    content = request.get_json()
    word = content['word']
    lang = content['lang']
    pos=content['pos']
    if pos=='*':
        pos=None

    # r=get_chains(word, lang=lang, pos=pos)
    # data_y = json.dumps(r)
    # return data_y
    return get_chains_as_json(lang, word, pos)

@cached(cache={})
def get_synsets_as_json(lang, raw_word, pos):
    from sagas.nlu.omw_extended import get_synsets
    try:
        word_parts=raw_word.split('/')  # 允许用'membaca/menbaca'形式
        for word in word_parts:
            sets = get_synsets(lang, word, pos)
            if len(sets)>0:
                r = [c.name() for c in sets]
                data_y = json.dumps(r)
                return data_y
    except Exception as e:
        logger.error(
            "Failed to get synsets for '{}'. "
            "Error: {}".format(raw_word, e))
    return '[]'

@app.route('/get_synsets', methods = ['POST'])
def handle_get_synsets():
    content = request.get_json()
    word = content['word']
    lang = content['lang']
    pos=content['pos']
    if pos=='*':
        pos=None

    # sets = get_synsets(lang, word, pos)
    # r=[c.name() for c in sets]
    # data_y = json.dumps(r)
    return get_synsets_as_json(lang, word, pos)

@app.route('/explore', methods = ['POST'])
def handle_explore():
    from sagas.nlu.wordnet_explore import explore
    content = request.get_json()
    word = content['word']
    lang = content['lang']
    targets=content['targets']

    rs=explore(word, lang=lang, target_langs=targets)
    data_y = json.dumps(rs)
    return data_y

@cached(cache={})
def get_word_sets_as_json(lang, raw_word, pos):
    try:
        procs = WordNetProcs()
        word_parts=raw_word.split('/')  # 允许用'membaca/menbaca'形式
        for word in word_parts:
            rs = procs.get_word_sets(word, lang, pos)
            if len(rs)>0:
                data_y = json.dumps(rs, ensure_ascii=False)
                return data_y
    except Exception as e:
        logger.error(
            "Failed to get wordsets for '{}'. "
            "Error: {}".format(raw_word, e))
    return '[]'

@app.route('/word_sets', methods = ['POST'])
def handle_word_sets():
    content = request.get_json()
    word = content['word']
    lang = content['lang']
    pos=content['pos']
    if pos=='*':
        pos=None

    # procs=WordNetProcs()
    # rs=procs.get_word_sets(word, lang, pos)
    # data_y = json.dumps(rs, ensure_ascii=False)
    # return data_y
    return get_word_sets_as_json(lang, word, pos)

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=8091, debug=True)
    app.run(host='0.0.0.0', port=8093)

