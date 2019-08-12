from flask import Flask
from flask import request
import json
from sagas.zh.ltp_procs import ltp

app = Flask(__name__)

def in_filters(val, filters):
    for f in filters:
        # if val.endswith(f):
        # support suffix, also support as 'nsubj:pass'
        if f in val:
            return True
    return False

def parse_sentence(sentence, filters):
    import sagas
    words = ltp.segmentor.segment(sentence)
    postags = ltp.postagger.postag(words)
    arcs = ltp.parser.parse(words, postags)
    roles = ltp.labeller.label(words, postags, arcs)
    netags = ltp.recognizer.recognize(words, postags)

    root = ''
    root_idx = 0
    collector = []
    verbs = []
    for i in range(len(words)):
        rel = arcs[i].relation
        pos = postags[i]
        if rel == 'HED':
            root = words[i]
            root_idx = i
        if pos == 'v':
            verbs.append(words[i])

    # print('root', root, root_idx)
    collector.append(('root', root))

    rs = []
    for i in range(len(words)):
        print("%s --> %s|%s|%s|%s" % (words[int(arcs[i].head) - 1], words[i], \
                                      arcs[i].relation, postags[i], netags[i]))
        pos = postags[i]
        dep_idx = int(arcs[i].head) - 1
        head = words[dep_idx]
        rel = arcs[i].relation
        rs.append((head, words[i], \
                   rel, pos, netags[i]))
        if dep_idx == root_idx and in_filters(rel, filters):
            collector.append((rel.lower(), words[i]))

    df = sagas.to_df(rs, ['弧头', '弧尾', '依存关系', '词性', '命名实体'])
    return df, collector, verbs

@app.route("/")
def home():
    return "servant: chinese"

@app.route('/digest', methods = ['POST'])
def handle_digest():
    """
    $ curl -XPOST -H 'Content-Type: application/json' -d '{"lang":"zh", "sents":"我是一个好老师"}'  http://localhost:8091/digest
    :return:
    """
    # print ("request is json?", request.is_json)
    content = request.get_json()
    sents=content['sents']
    lang=content['lang']
    print (lang, sents)
    df, collector, verbs = parse_sentence(sents, ['SBV', 'OB'])
    data = {'lang': lang}
    for el in collector:
        data[el[0]]=el[1]
    data['verbs']=verbs

    # data_y=yaml.dump(data, default_flow_style=True,Dumper=KludgeDumper,encoding=None)
    data_y = json.dumps(data, ensure_ascii=False)
    return data_y

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=8091, debug=True)
    app.run(host='0.0.0.0', port=8091)

