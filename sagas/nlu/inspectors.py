import time
import requests
import json
from sagas.nlu.inspector_common import Inspector, Context
from sagas.nlu.inspector_fixtures import InspectorFixture
from sagas.nlu.patterns import Patterns, print_result
import logging
logger = logging.getLogger('inspector')

current_milli_time = lambda: int(round(time.time() * 1000))
locale_mappings={'en':'en_GB', 'ru':'ru_Nothing',
                 'es':'es_Nothing', 'fr':'fr_Nothing',
                 'de':'de_Nothing', 'ja':'ja_Nothing',
                 'zh':'zh_CN', 'ar':'ar_Nothing',
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
    """
    Testcases:
        $ ses 'Nosotros comíamos con la familia para Navidad.'
    """
    def __init__(self, dims, provider='duckling'):
        if isinstance(dims, str):
            self.dims = {dims}
        else:
            self.dims=dims
        self.fits=lambda ds: any([c in ds for c in self.dims])
        self.provider=provider
        self.providers={'duckling':self.duckling_provider,
                        'snips': self.snips_provider,
                        }
        self.parsers={}

    def name(self):
        return "ins_date"

    def duckling_provider(self, cnt, lang, ctx, key):
        result = False
        logger.debug('query with duckling: %s', cnt)
        resp = query_duckling(cnt, lang)
        if resp['result'] == 'success':
            logger.debug(json.dumps(resp, indent=2, ensure_ascii=False))
            dims = [d['dim'] for d in resp['data']]
            logger.debug('dims: %s', dims)
            # if self.dim in dims:
            if self.fits(dims):
                result = True
                ctx.add_result(self.name(), self.provider, key, resp['data'])
        return result

    def snips_provider(self, cnt, lang, ctx, key):
        from snips_nlu_parsers import BuiltinEntityParser
        result = False
        if lang in self.parsers:
            parser = self.parsers[lang]
        else:
            parser = BuiltinEntityParser.build(language=lang)
            self.parsers[lang] = parser
        parsing = parser.parse(cnt)
        dims = [d['entity_kind'] for d in parsing]
        print(cnt, '->', 'dims', dims, 'to fits in', self.dims)
        if self.fits(dims):
            result = True
            ctx.add_result(self.name(), self.provider, key, parsing)
        return result

    def run(self, key, ctx:Context):
        checkers = []
        lang = ctx.meta['lang']
        # cnt = ' '.join(ctx.chunks['obl'])
        # cnt = ' '.join(ctx.chunks[key])

        for cnt in ctx.chunk_pieces(key):
            checkers.append(self.providers[self.provider](cnt, lang, ctx, key))
        # print('... put %s'%self.cache_key(key))
        # print(ctx.meta['intermedia'])
        return any(checkers)

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

def query_entities_by_url(url, data):
    response = requests.post(url, json=data)
    if response.status_code == 200:
        r=response.json()
        return {'result':'success', 'data':r}
    return {'result':'fail', 'cause':'error response'}

def query_entities(data):
    return query_entities_by_url('http://localhost:8092/entities', data)

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
        requestors={'ru':lambda rc: query_entities_by_url('http://localhost:8095/entities', rc),
                    }
        for cnt in ctx.chunk_pieces(key):
            data={'lang': lang, 'sents': cnt}
            if lang in requestors:
                resp=requestors[lang](data)
            else:
                resp = query_entities(data)
            if resp['result'] == 'success':
                dims = [d['entity'] for d in resp['data']]
                # print('entities ->', ', '.join(dims))
                logger.info('entities -> %s, self.dim -> %s', ', '.join(dims), self.dim)
                if self.dim in dims:
                    print('\t%s ∈' % cnt, self.dim)
                    result = True
        return result

    def __str__(self):
        return "{}('{}')".format(self.name(), self.dim)

class Inspectors(InspectorFixture):
    def procs_common(self, data, print_format='table', engine='corenlp'):
        domains, meta=self.request_domains(data, print_format, engine)
        if domains is None:
            print('! request_domains returns empty.')
        else:
            agency = ['c_pron', 'c_noun']
            rs = [Patterns(domains, meta, 1).verb(nsubj=agency, obj=agency),
                  Patterns(domains, meta, 2).verb(nsubj=agency, obj=agency, advmod=NegativeWordInspector()),
                  Patterns(domains, meta, 2).verb(nsubj_pass=agency, obl=DateInspector('time')),
                  Patterns(domains, meta, 2).verb(nsubj_pass=agency, obl=EntityInspector('GPE')),
                  Patterns(domains, meta, 5).verb(nsubj=agency, obl=EntityInspector('location')),
                  Patterns(domains, meta, 2).verb(obl=PlainInspector()),
                  ]
            print_result(rs)

    def ents(self, sents, lang='en'):
        """
        $ python -m sagas.nlu.inspectors ents 'I am from China'
        $ python -m sagas.nlu.inspectors ents 'Россия, Вологодская обл. г. Череповец, пр.Победы 93 б' ru
        $ python -m sagas.nlu.inspectors ents 'Я работаю в китае.' ru
        :param sents:
        :param lang:
        :return:
        """
        # ents = query_entities({"lang": "en", "sents": "I am from China"})
        data={"lang": lang, "sents": sents}
        if lang=='ru':
            ents=query_entities_by_url('http://localhost:8095/entities', data)
        else:
            ents = query_entities(data)
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
        import sagas.nlu.patterns as pats
        pats.print_not_matched=True
        texts = [('en', 'I was born in Beijing in the spring of 1982.'),
                 ('ru', 'Я работаю в китае.'),
                 ]
        for text in texts:
            data = {'lang': text[0], "sents": text[1]}
            self.procs_common(data)

    def test_3(self):
        text = 'Han har ikke tøjet på.'
        data = {'lang': 'da', "sents": text}
        self.procs_common(data)

if __name__ == '__main__':
    import fire
    fire.Fire(Inspectors)

