import time
import requests
import json
from sagas.nlu.inspector_common import Inspector, Context
from sagas.nlu.inspector_fixtures import InspectorFixture
from sagas.nlu.patterns import Patterns, print_result
import logging
logger = logging.getLogger(__name__)

current_milli_time = lambda: int(round(time.time() * 1000))
locale_mappings={'en':'en_GB', 'ru':'ru_Nothing',
                 'es':'es_Nothing', 'fr':'fr_Nothing',
                 'de':'de_Nothing', 'ja':'ja_Nothing',
                 'zh':'zh_CN'
                }

def query_duckling(text, lang):
    """
    resp=query_duckling('tomorrow at eight', 'en')
    print([d['dim'] for d in resp['data']])

    :param text:
    :param lang:
    :return:
    """
    if lang in locale_mappings:
        locale=locale_mappings[lang]
    else:
        return {'result':'fail', 'cause':"unsupport lang"}
    data={'locale':locale, 'text':text, 'reftime':current_milli_time()}
    response = requests.post('http://0.0.0.0:8000/parse', data=data)
    if response.status_code == 200:
        r=response.json()
        # print(json.dumps(r, indent=2, ensure_ascii=False))
        return {'result':'success', 'data':r}
    return {'result':'fail', 'cause':'error response'}

class DateInspector(Inspector):
    def __init__(self, dim):
        self.dim = dim

    def name(self):
        return "ins_date"

    def run(self, key, ctx:Context):
        result = False
        lang = ctx.meta['lang']
        # cnt = ' '.join(ctx.chunks['obl'])
        # cnt = ' '.join(ctx.chunks[key])

        for cnt in ctx.chunk_pieces(key):
            logger.info('query with duckling: %s', cnt)
            resp = query_duckling(cnt, lang)
            if resp['result'] == 'success':
                if self.dim in [d['dim'] for d in resp['data']]:
                    result = True
        # print('... put %s'%self.cache_key(key))
        # print(ctx.meta['intermedia'])
        return result

class NegativeWordInspector(Inspector):
    def name(self):
        return "ins_negative_word"

    def run(self, key, ctx:Context):
        result=False
        # domains=dispatcher.domains
        if ctx.meta['lang']=='da':
            # if 'ikke' in ctx.chunks[key] or 'ikke'==ctx.lemmas[key]:
            if ctx.chunk_contains(key, 'ikke') or 'ikke' == ctx.lemmas[key]:
                result=True
        elif ctx.meta['lang']=='de':
            if ctx.chunk_contains(key, 'nicht') or 'nicht' == ctx.lemmas[key]:
                result=True
        return result

class PlainInspector(Inspector):
    def name(self):
        return "plain"

    def run(self, key, ctx:Context):
        result=False
        print(key, ctx.stem_pieces(key))
        return result

def query_entities(data):
    response = requests.post('http://localhost:8092/entities', json=data)
    if response.status_code == 200:
        r=response.json()
        return {'result':'success', 'data':r}
    return {'result':'fail', 'cause':'error response'}

class EntityInspector(Inspector):
    def __init__(self, dim):
        self.dim = dim

    def name(self):
        return "ins_entity"

    def run(self, key, ctx:Context):
        result = False
        lang = ctx.meta['lang']
        # cnt = ' '.join(ctx.chunks[key])
        # cnt=ctx.get_single_chunk_text(key)
        for cnt in ctx.chunk_pieces(key):
            resp = query_entities({'lang': lang, 'sents': cnt})
            if resp['result'] == 'success':
                dims = [d['entity'] for d in resp['data']]
                # print('entities ->', ', '.join(dims))
                logger.info('entities -> %s', ', '.join(dims))
                if self.dim in dims:
                    print('\t%s ∈' % cnt, self.dim)
                    result = True
        return result

class Inspectors(InspectorFixture):
    def procs_common(self, data):
        domains, meta=self.request_domains(data)
        agency = ['c_pron', 'c_noun']
        rs = [Patterns(domains, meta, 1).verb(nsubj=agency, obj=agency),
              Patterns(domains, meta, 2).verb(nsubj=agency, obj=agency, advmod=NegativeWordInspector()),
              Patterns(domains, meta, 2).verb(nsubj_pass=agency, obl=DateInspector('time')),
              Patterns(domains, meta, 2).verb(nsubj_pass=agency, obl=EntityInspector('GPE')),
              Patterns(domains, meta, 2).verb(obl=PlainInspector()),
              ]
        print_result(rs)

    def ents(self, sents, lang='en'):
        # ents = query_entities({"lang": "en", "sents": "I am from China"})
        ents = query_entities({"lang": lang, "sents": sents})
        print(ents)

    def test_1(self):
        """
        $ python -m sagas.nlu.inspectors test_1
        :return:
        """
        text = 'I was born in Beijing.'
        data = {'lang': 'en', "sents": text}
        self.procs_common(data)

    def test_2(self):
        """
        $ python -m sagas.nlu.inspectors test_2
        :return:
        """
        text = 'I was born in Beijing in the spring of 1982.'
        data = {'lang': 'en', "sents": text}
        self.procs_common(data)

    def test_3(self):
        text = 'Han har ikke tøjet på.'
        data = {'lang': 'da', "sents": text}
        self.procs_common(data)

if __name__ == '__main__':
    import fire
    fire.Fire(Inspectors)

