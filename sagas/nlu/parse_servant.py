from flask import Flask
from flask import request
import json
from cachetools import cached, TTLCache
import logging

from sagas.nlu.multilang_servant import multilang

logger = logging.getLogger('servant')

# nlp=langs['de']()
app = Flask(__name__)
app.register_blueprint(multilang)

def get_doc_verbs(doc):
    return [(word.text, word.lemma) for sent in
                doc.sentences for word in sent.words if word.upos=='VERB']
def get_doc_root(doc):
    root=''
    segs=doc.sentences[0]
    for dep_edge in segs.dependencies:
        # print(dep_edge[2].text, dep_edge[0].index, dep_edge[1])
        if dep_edge[1]=='root':
            root=dep_edge[2].text
    return root

def get_doc_root_and_idx(doc):
    root=''
    root_idx=0
    cur=1  ## word index starts with 1
    segs=doc.sentences[0]
    for dep_edge in segs.dependencies:
        # print(dep_edge[2].text, dep_edge[0].index, dep_edge[1])
        if dep_edge[1]=='root':
            root=dep_edge[2].text
            root_idx=cur
        cur=cur+1
    return root, root_idx

def in_filters(val, filters):
    for f in filters:
        # if val.endswith(f):
        # support suffix, also support as 'nsubj:pass'
        if f in val:
            return True
    return False

def get_root_rel(doc, root_idx, filters):
    segs=doc.sentences[0]
    rs=[]
    for dep_edge in segs.dependencies:
        print(dep_edge[2].text, dep_edge[0].index, str(dep_edge[1]))
        # if dep_edge[0].index==str(root_idx) and str(dep_edge[1]) in filters:
        # if dep_edge[0].index==str(root_idx):
        if dep_edge[0].index==str(root_idx) and in_filters(str(dep_edge[1]), filters):
            rs.append((dep_edge[1], dep_edge[2].text))
    return rs

def json_to_string(obj, **kwargs):
    indent = kwargs.pop("indent", 2)
    ensure_ascii = kwargs.pop("ensure_ascii", False)
    return json.dumps(obj, indent=indent, ensure_ascii=ensure_ascii, **kwargs)

@app.route("/")
def home():
    return "servant: german"

@app.route('/digest', methods = ['POST'])
def handle_digest():
    """
    $ curl -XPOST -H 'Content-Type: application/json' -d '{"sents":"Die Eltern mögen den Käse."}'  http://localhost:8090/digest
    will get: {"root": "mögen", "verbs": [["mögen", "mögen"]]}
    :return:
    """
    from sagas.nlu.corenlp_helper import CoreNlp, CoreNlpViz, get_nlp

    # print ("request is json?", request.is_json)
    content = request.get_json()
    sents=content['sents']
    lang=content['lang']
    print (lang, sents)
    # dumped = json_to_string({"ok": 'JSON posted'})
    nlp=get_nlp(lang)
    doc = nlp(sents)
    root, root_idx = get_doc_root_and_idx(doc)

    # subj(nsubj), obj(iobj, dobj, pobj)
    # pobj : object of a preposition，介词的宾语
    # obl类似pobj, obl关系用于名义（名词，代词，名词短语），作为非核心（倾斜）参数或附件。
    # 这意味着它在功能上对应于附加在动词，形容词或其他副词上的状语。
    rs = get_root_rel(doc, root_idx, ['subj', 'obj', 'cop', 'obl'])
    data = {'lang': lang, 'root': root, 'verbs': get_doc_verbs(doc)}
    for el in rs:
        data[el[0]]=el[1]
    # data_y=yaml.dump(data, default_flow_style=True,Dumper=KludgeDumper,encoding=None)
    data_y = json.dumps(data, ensure_ascii=False)
    return data_y

def fix_sents(lang, text):
    # if lang in ['de', 'pt']:
    if lang not in ['zh', 'zh-CN', 'zh-TW', 'ja',
                    'ar', 'fa', 'ur', 'he']:
        text=text.strip()
        if text[-1] not in ['!','?','.']:
            return '%s .'%text
        if text[-2]!=' ':
            return '%s %s'%(text[0:-1], text[-1])
    return text

def is_disabled(opts, opt):
    if opt in opts:
        return opts[opt]
    return False

# verb_domains
@app.route('/verb_domains', methods = ['POST'])
def handle_verb_domains():
    # from sagas.nlu.corenlp_parser import get_verb_domain, get_aux_domain, get_subj_domain
    from sagas.nlu.corenlp_parser import get_chunks
    from sagas.nlu.uni_cli import parse_with

    content = request.get_json()
    sents = content['sents']
    lang = content['lang']
    if 'engine' in content:
        engine=content['engine']
    else:
        engine='corenlp'

    sents=fix_sents(lang, sents)

    # nlp = get_nlp(lang)
    # doc = nlp(sents)
    # sent = doc.sentences[0]
    logger.debug(f".. parse sents [{sents}] with engine {engine} in lang {lang}")
    sent=parse_with(sents, lang, engine=engine)

    # r = get_verb_domain(sent, ['obl', 'nsubj:pass'])
    # if len(r)==0:
    #     r=get_aux_domain(sent, ['obl', 'nsubj:pass'])
    # if len(r)==0:
    #     r = get_subj_domain(sent)

    disable_predicts=is_disabled(content, 'disable_predicts')
    predicts_count=len(sent.predicts)
    if predicts_count>0 and not disable_predicts:
        r= sent.predicts
    else:
        logger.debug(f"predicts count is {predicts_count}, option disable_predicts is {disable_predicts}")
        r= get_chunks(sent)
    data_y = json.dumps(r, ensure_ascii=False)
    return data_y

def invoke_parser(sents, lang, engine, pipelines, func):
    # content = request.get_json()
    sents = fix_sents(lang, sents)
    r = func(sents, lang, engine, pipelines)
    data_y = json.dumps(r, ensure_ascii=False)
    return data_y

@cached(cache={})
def parse_sents(raw):
    from sagas.nlu.uni_jsonifier import jsonify_pipelines
    content=json.loads(raw)
    print('.. only print once', content)
    sents = content['sents']
    lang = content['lang']
    if 'engine' in content:
        engine = content['engine']
    else:
        engine = 'corenlp'
    if 'pipelines' in content:
        pipelines = content['pipelines']
    else:
        pipelines = []
    return invoke_parser(sents, lang, engine, pipelines,
                         lambda s, l, e, p: jsonify_pipelines(s, l, e, p))

@app.route('/dep_parse', methods = ['POST'])
def handle_dep_parse():
    # from sagas.nlu.uni_jsonifier import jsonify_pipelines
    # return invoke_parser(request, lambda s,l,e,p: jsonify_pipelines(s,l,e,p))

    # content=request.get_json()
    content=request.get_data(as_text=True)
    print('..', content)
    return parse_sents(content)

class ParseServant(object):
    def __init__(self):
        pass

    def dev(self, port=14000):
        app.run(host='0.0.0.0', port=port)

    def run(self, port=14000):
        from waitress import serve
        serve(app, host='0.0.0.0', port=port)

if __name__ == "__main__":
    import fire
    from sagas.tool.loggers import init_logger

    init_logger()
    # app.run(debug=True)
    # app.run(host='0.0.0.0', port=8090, debug=True)
    # app.run(host='0.0.0.0', port=8090)
    fire.Fire(ParseServant)


