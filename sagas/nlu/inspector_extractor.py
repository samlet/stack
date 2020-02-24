from typing import Text, Any, Dict, List
import requests

from sagas.nlu.inspector_common import Inspector, Context
import logging
logger = logging.getLogger(__name__)

class CompExtractInspector(Inspector):
    """
    提取指定成分:
    >>> pat(3, name='extract_day').cop(behaveof('day', 'n'),
                                              flat=kindof('feast_day/day', 'n'),
                                              nsubj=extract('plain+date_search+date_parse')),
    """
    def __init__(self, comp_as='plain', pickup=None):
        self.comp_as=comp_as.split('+')
        self.pickup=pickup
        # key是成分名, value是tuple-list, element-0为判定名, element-1为结果
        self.results={}

    def name(self):
        return "extract_comps"

    def run(self, key, ctx:Context):
        # 当pickup为'_'时, key就是value
        comp_val=key if self.pickup=='_' else ''
        key=self.pickup or key

        def ex_date_search(cnt, comp):
            from dateparser.search import search_dates
            search_r = search_dates(cnt, languages=[ctx.lang])
            if search_r is not None:
                ctx.add_result(self.name(), comp, key, [str(r) for r in search_r])
                return True
            return False
        def ex_date_parse(cnt, comp):
            from dateparser import parse
            parse_r = parse(cnt, languages=[ctx.lang])
            if parse_r is not None:
                ctx.add_result(self.name(), comp, key, str(parse_r))
                return True
            return False
        def ex_plain(cnt, comp):
            ctx.add_result(self.name(), comp, key, cnt)
            return True
        def ex_translit(cnt, comp):
            from sagas.nlu.transliterations import translits
            if translits.is_available_lang(ctx.lang):
                tval= translits.translit(cnt, ctx.lang)
                # tval=tval.replace('[UNK]', '').strip()
                ctx.add_result(self.name(), comp, key, tval)
            else:
                ctx.add_result(self.name(), comp, key, cnt)
            return True
        def ex_dims(cnt, comp, dim):
            from sagas.nlu.inspectors import query_duckling
            resp = query_duckling(cnt, ctx.lang)
            # print('*************', cnt, ctx.lang, resp)
            values=[d for d in resp['data'] if d['dim']==dim]
            if len(values)>0:
                ctx.add_result(self.name(), comp, key, values)
                return True
            return False
        def ex_rasa(cnt, comp):
            from sagas.conf.conf import cf
            from sagas.nlu.rasa_procs import invoke_nlu

            endpoint = cf.ensure('nlu_multilang_servant')
            result = invoke_nlu(endpoint, ctx.lang, "current", ctx.sents)
            # print('*******', result)
            if result != None:
                ctx.add_result(self.name(), comp, 'sents', result)
                return True
            return False
        def ex_chunk(cnt, comp, clo):
            from sagas.nlu.uni_chunks import get_chunk
            from sagas.nlu.ruleset_procs import list_words, cached_chunks
            from sagas.conf.conf import cf
            # get_chunk(f'verb_domains', 'xcomp/obj', lambda w: w.upos)
            chunks = cached_chunks(ctx.sents, ctx.lang, cf.engine(ctx.lang))
            parts=self.pickup.split(':')
            domain=parts[0]
            path=parts[1]
            result = get_chunk(chunks, f'{domain}_domains', path, clo=clo)
            logger.debug(f"extract chunk: {domain}, {path}, {result}")
            if len(result)>0:
                ctx.add_result(self.name(), comp, self.pickup, result)
                return True
            return False
        def ex_ner(cnt, comp):
            data = {"sents": ctx.sents if self.pickup=='_' else cnt}
            route=f'spacy/{ctx.lang}' if ctx.lang in ('zh', 'ru', 'ja', 'id') else ctx.lang
            response = requests.post(f'http://localhost:1700/ner/{route}', json=data)
            if response.status_code==200:
                result=response.json()
                if len(result)>0:
                    ctx.add_result(self.name(), comp, self.pickup, result)
                    return True
            return False

        ex_map={'date_search': ex_date_search,
                'date_parse': ex_date_parse,
                'plain': ex_plain,
                'translit': ex_translit,
                'email': lambda cnt,comp: ex_dims(cnt, comp, 'email'),
                'number': lambda cnt, comp: ex_dims(cnt, comp, 'number'),
                'time': lambda cnt, comp: ex_dims(cnt, comp, 'time'),
                'temperature': lambda cnt, comp: ex_dims(cnt, comp, 'temperature'),
                # example: extract_for('rasa', '_')
                'rasa': lambda cnt, comp: ex_rasa(cnt, comp),
                # example: extract_for('chunk', 'verb:xcomp/obj')
                'chunk': lambda cnt, comp: ex_chunk(cnt, comp, lambda w: (w.text, w.upos.lower())),
                # example: extract_for('chunk_text', 'verb:xcomp/obj')
                'chunk_text': lambda cnt, comp: ex_chunk(cnt, comp, lambda w: w.text),
                # example: extract_for('ner', '_'), extract_for('ner', 'xcomp')
                'ner': lambda cnt, comp: ex_ner(cnt, comp),
                }

        if self.pickup=='_' or ':' in self.pickup:
            self.results['_']=[]
            for comp in self.comp_as:
                op=ex_map[comp](comp_val, comp)
                self.results['_'].append((comp,op))
        else:
            for cnt in ctx.chunk_pieces(key):
                self.results[key]=[]
                for comp in self.comp_as:
                    ex=ex_map[comp]
                    op=ex(cnt, comp)
                    # self.results[comp] = op
                    self.results[key].append((comp, op))

        return True  # 只负责提取, 并不参与判定, 所以始终返回True

    @property
    def after(self):
        return True

    def __str__(self):
        return f"ins_{self.name()}({self.comp_as})"

extract=lambda c='plain': CompExtractInspector(c)
extract_dt=lambda c='plain+date_search+date_parse': CompExtractInspector(c)
extract_c=lambda p: CompExtractInspector('plain', p)
extract_for=lambda f, p: CompExtractInspector(f, p)

