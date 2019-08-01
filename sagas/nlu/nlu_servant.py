from flask import Flask
from flask import request
import json

app = Flask(__name__)

def spacy_doc(sents, lang):
    from sagas.nlu.spacy_helper import spacy_mgr
    spacy_nlp = spacy_mgr.get_model(lang)
    return spacy_nlp(sents)

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
    content = request.get_json()
    sents=content['sents']
    lang=content['lang']
    print (lang, sents)

    # data = {'lang': lang}
    rs = []
    doc = spacy_doc(sents, lang)
    for ent in doc.ents:
        rs.append({'text': ent.text,
                   'start': ent.start_char,
                   'end': ent.end_char,
                   'entity': ent.label_})

    # data_y=yaml.dump(data, default_flow_style=True,Dumper=KludgeDumper,encoding=None)
    data_y = json.dumps(rs, ensure_ascii=False)
    return data_y

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=8091, debug=True)
    app.run(host='0.0.0.0', port=8092)

