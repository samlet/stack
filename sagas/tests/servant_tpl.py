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
    $ curl -XPOST -H 'Content-Type: application/json' -d '{"lang":"zh", "sents":"我是一个好老师"}'  http://localhost:15001/digest
    :return:
    """
    print("request is json?", request.is_json)
    content = request.get_json()
    sents=content['sents']
    lang=content['lang']
    print(lang, sents)

    data = {'lang': lang}

    # data_y=yaml.dump(data, default_flow_style=True,Dumper=KludgeDumper,encoding=None)
    data_y = json.dumps(data, ensure_ascii=False)
    return data_y

class SimpleServant(object):
    def __init__(self, port=15001):
        self.port=port

    def dev(self):
        """
        $ python -m sagas.tests.servant_tpl dev
        :return:
        """
        app.run(host='0.0.0.0', port=self.port, debug=True)

    def run(self):
        from waitress import serve
        serve(app, host='0.0.0.0', port=self.port)

if __name__ == "__main__":
    import fire
    from sagas.tool.loggers import init_logger

    init_logger()
    fire.Fire(SimpleServant)
