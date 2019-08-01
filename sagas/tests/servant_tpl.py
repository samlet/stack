from flask import Flask
from flask import request
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "servant: nlu"

@app.route('/digest', methods = ['POST'])
def handle_digest():
    """
    $ curl -XPOST -H 'Content-Type: application/json' -d '{"lang":"zh", "sents":"我是一个好老师"}'  http://localhost:8092/digest
    :return:
    """
    # print ("request is json?", request.is_json)
    content = request.get_json()
    sents=content['sents']
    lang=content['lang']
    print (lang, sents)

    data = {'lang': lang}

    # data_y=yaml.dump(data, default_flow_style=True,Dumper=KludgeDumper,encoding=None)
    data_y = json.dumps(data, ensure_ascii=False)
    return data_y

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=8091, debug=True)
    app.run(host='0.0.0.0', port=8092)

