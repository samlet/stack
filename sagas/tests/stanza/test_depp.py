"""
$ pytest -s -v test_depp.py
"""
import stanza
from stanza import Document
from stanza.models.common.doc import Sentence
from sagas.conf.conf import cf

def test_en():
    pipeline = stanza.Pipeline(dir=f'{cf.conf_dir}/ai/corenlp/1.0', package='default', lang='en')
    doc:Document = pipeline('I was born in Beijing.')
    sent:Sentence=doc.sentences[0]
    sent.print_tokens()
    sent.print_dependencies()
    print(doc.entities)

def test_zh():
    pipeline_zh = stanza.Pipeline(dir=f'{cf.conf_dir}/ai/corenlp/1.0', package='default', lang='zh-hans')
    doc:Document = pipeline_zh('我明天去上班')
    doc.sentences[0].print_tokens()
    doc.sentences[0].print_dependencies()
    print(doc.entities)

