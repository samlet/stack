from typing import Text, Dict

from flask import Flask
from flask import request
import json
import logging
from cachetools import cached
from sagas.nlu.net_context import EntitiesRequest

logger = logging.getLogger(__name__)
app = Flask(__name__)

def spacy_doc(sents, lang):
    from sagas.nlu.spacy_helper import spacy_mgr
    spacy_nlp = spacy_mgr.get_model(lang)
    return spacy_nlp(sents)

@cached(cache={})
def analyse_doc(sents:Text, lang:Text):
    from sagas.nlu.spacy_helper import is_available

    if not is_available(lang):
        logging.warning(f"lang {lang} is unavaiable in entity extractor.")
        return []

    rs = []
    doc = spacy_doc(sents, lang)
    for ent in doc.ents:
        rs.append({'text': ent.text,
                   'start': ent.start_char,
                   'end': ent.end_char,
                   'entity': ent.label_})
    return rs

def spacy_ner(req_json):
    ctx = EntitiesRequest(req_json)
    return analyse_doc(ctx.sents, ctx.lang)

@app.route("/")
def home():
    return "servant: nlu"

@app.route('/entities', methods = ['POST'])
def handle_entities():
    """
    $ curl -XPOST -H 'Content-Type: application/json' -d '{"lang":"en", "sents":"I am from China"}'  http://localhost:8092/entities
    :return:
    """
    # print ("request is json?", request.is_json)
    # content = request.get_json()
    # sents=content['sents']
    # lang=content['lang']
    # print (lang, sents)

    # data_y=yaml.dump(data, default_flow_style=True,Dumper=KludgeDumper,encoding=None)
    # data_y = json.dumps(rs, ensure_ascii=False)
    # return data_y
    return EntitiesRequest.wrap_result(spacy_ner(request.get_json()))

# @app.route('/word_sets', methods = ['POST'])
# def handle_word_sets():
#     from sagas.nlu.wordnet_procs import WordNetProcs
#
#     content = request.get_json()
#     word = content['word']
#     lang = content['lang']
#
#     procs=WordNetProcs()
#     rs=procs.get_word_sets(word, lang)
#     data_y = json.dumps(rs, ensure_ascii=False)
#     return data_y

if __name__ == "__main__":
    from sagas.tool.loggers import init_logger
    # app.run(host='0.0.0.0', port=8091, debug=True)
    init_logger()
    app.run(host='0.0.0.0', port=8092)

