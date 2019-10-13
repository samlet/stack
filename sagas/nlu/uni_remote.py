from sagas.nlu.uni_intf import SentenceIntf
from sagas.nlu.uni_jsonifier import JsonifySentImpl
import requests
import json
from sagas.conf.conf import cf
import sagas.tracker_fn as tc

def dep_parse(sents, lang='en', engine='corenlp', pipelines=None)-> (SentenceIntf, dict):
    if pipelines is None:
        pipelines = []
    data = {'lang': lang, "sents": sents, 'engine': engine, 'pipelines':pipelines}
    tc.info(f".. request is {data}")
    response = requests.post(f'{cf.servant(engine)}/dep_parse', json=data)
    if response.status_code != 200:
        tc.info('.. dep_parse servant invoke fail.')
        return None, None

    result = response.json()
    words=result['sents']
    if len(words) == 0:
        tc.info('.. dep_parse servant returns empty set.')
        tc.info('.. request data is', data)
        return None, None

    doc_jsonify = JsonifySentImpl(words)
    if len(pipelines)>0:
        result_set={p:result[p] for p in pipelines}
        return doc_jsonify, result_set
    return doc_jsonify, None

