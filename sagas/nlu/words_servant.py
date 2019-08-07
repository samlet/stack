from flask import Flask
from flask import request
import json
from sagas.nlu.wordnet_procs import WordNetProcs, predicate_chain, get_chains

app = Flask(__name__)

@app.route("/")
def home():
    return "servant: words"

@app.route('/predicate', methods = ['POST'])
def handle_predicate():
    content = request.get_json()
    word = content['word']
    lang = content['lang']
    pos=content['pos']
    if pos=='*':
        pos=None

    procs=WordNetProcs()
    r=procs.predicate(word, content['kind'], lang=lang, pos=pos, only_first=content['only_first'])
    data_y = json.dumps({'result':r})
    return data_y

@app.route('/predicate_chain', methods = ['POST'])
def handle_predicate_chain():
    content = request.get_json()
    word = content['word']
    lang = content['lang']
    pos=content['pos']
    if pos=='*':
        pos=None

    r,c=predicate_chain(word, content['kind'], lang=lang, pos=pos)
    data_y = json.dumps({'result':r, 'data':c})
    return data_y

@app.route('/get_chains', methods = ['POST'])
def handle_get_chains():
    content = request.get_json()
    word = content['word']
    lang = content['lang']
    pos=content['pos']
    if pos=='*':
        pos=None

    r=get_chains(word, lang=lang, pos=pos)
    data_y = json.dumps(r)
    return data_y

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

@app.route('/word_sets', methods = ['POST'])
def handle_word_sets():
    content = request.get_json()
    word = content['word']
    lang = content['lang']
    pos=content['pos']
    if pos=='*':
        pos=None

    procs=WordNetProcs()
    rs=procs.get_word_sets(word, lang, pos)
    data_y = json.dumps(rs, ensure_ascii=False)
    return data_y

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=8091, debug=True)
    app.run(host='0.0.0.0', port=8093)

