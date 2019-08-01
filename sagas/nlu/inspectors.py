from sagas.nlu.patterns import Inspector
import time
import requests
import json

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
    data={'locale':'en_GB', 'text':text, 'reftime':current_milli_time()}
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

    def run(self, key, ctx):
        result = False
        lang = ctx.meta['lang']
        cnt = ' '.join(ctx.chunks['obl'])
        print(cnt)
        resp = query_duckling(cnt, lang)
        if resp['result'] == 'success':
            if self.dim in [d['dim'] for d in resp['data']]:
                result = True
        return result

class NegativeWordInspector(Inspector):
    def name(self):
        return "ins_negative_word"

    def run(self, key, ctx):
        result=False
        # domains=dispatcher.domains
        if ctx.meta['lang']=='da':
            if 'ikke' in ctx.chunks[key] or 'ikke'==ctx.lemmas[key]:
                result=True
        return result

