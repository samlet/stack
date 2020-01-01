from sanic import Blueprint
from sanic.response import json

ner_mod = Blueprint('ner', url_prefix='/ner')

@ner_mod.post('/spacy/<lang>')
async def handle_spacy_ner(request, lang):
    """
    $ curl -d '{"sents":"I was born in Beijing."}' \
        -H "Content-Type: application/json" -X POST \
        localhost:1700/ner/spacy/en | json
      > [
          {
            "text": "Beijing",
            "start": 14,
            "end": 21,
            "entity": "GPE"
          }
        ]

    :param request:
    :param lang:
    :return:
    """
    from sagas.nlu.nlu_servant import analyse_doc
    rd=request.json
    return json(analyse_doc(rd['sents'], lang))

@ner_mod.post('/ru')
async def handle_ru(request):
    """
    $ curl -d '{"sents":"Россия, Вологодская обл. г. Череповец, пр.Победы 93 б"}' \
        -H "Content-Type: application/json" -X POST \
        localhost:1700/ner/ru | json
    :param request:
    :return:
    """
    from sagas.nlu.multilang_servant import extract_ru
    rd = request.json
    return json(extract_ru(rd['sents']))

@ner_mod.post('/ja')
async def handle_ja(request):
    """
    $ curl -d '{"sents":"太郎は5月18日の朝9時に花子に会いに行った"}' \
        -H "Content-Type: application/json" -X POST \
        localhost:1700/ner/ja | json
    :param request:
    :return:
    """
    from sagas.ja.knp_ner import ner
    rd = request.json
    return json(ner(rd['sents']))

@ner_mod.post('/zh')
async def handle_zh(request):
    """
    命名实体说明: ltp命名实体类型为：人名（Nh），地名（NS），机构名（Ni）；
    ltp采用BIESO标注体系。B表示实体开始词，I表示实体中间词，E表示实体结束词，
    S表示单独成实体，O表示不构成实体。

    $ curl -s -d '{"sents":"我在北京工作"}' \
        -H "Content-Type: application/json" -X POST \
        localhost:1700/ner/zh | json
      > [
          {
            "start": 2,
            "end": 4,
            "text": "北京",
            "entity": "S-Ns"
          }
        ]

    :param request:
    :return:
    """
    from sagas.zh.ltp_ner import ltp_ner
    rd = request.json
    return json(ltp_ner(rd['sents']))

@ner_mod.post('/zh/jieba')
async def handle_jieba(request):
    """
    $ curl -s -d '{"sents":"Rami Eid正在纽约石溪大学学习"}' \
        -H "Content-Type: application/json" -X POST \
        localhost:1700/ner/zh/jieba | json

    :param request:
    :return:
    """
    from sagas.zh.jieba_procs import extract_entities
    rd = request.json
    return json(extract_entities(rd['sents']))

@ner_mod.post('/id')
async def handle_id(request):
    """
    $ curl -d '{"sents":"Jokowi pergi ke Singapura."}' \
        -H "Content-Type: application/json" -X POST \
        localhost:1700/ner/id | json
    :param request:
    :return:
    """
    from sagas.id.indonesia_ner import id_ner
    rd = request.json
    return json(id_ner.ner(rd['sents']))

