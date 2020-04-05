from typing import Text, Any, Dict, List
import requests

from sagas.nlu.inspector_common import Inspector, Context, cla_meta_intf
import logging

from sagas.nlu.utils import is_full_domain_path

logger = logging.getLogger(__name__)

extractor="extract_comps"
def ex_date_search(key, cnt:Text, comp, ctx:cla_meta_intf):
    from dateparser.search import search_dates
    search_r = search_dates(cnt, languages=[ctx.lang])
    if search_r is not None:
        ctx.add_result(extractor, comp, key, [str(r) for r in search_r])
        return True
    return False


def ex_date_parse(key, cnt, comp, ctx:cla_meta_intf):
    from dateparser import parse
    parse_r = parse(cnt, languages=[ctx.lang])
    if parse_r is not None:
        ctx.add_result(extractor, comp, key, str(parse_r))
        return True
    return False


def ex_plain(key:Text, cnt:Text, comp:Text, ctx:cla_meta_intf):
    ctx.add_result(extractor, comp, key, cnt)
    return True


def ex_word(key:Text, cnt:Text, comp:Text, ctx:Context):
    ctx.add_result(extractor, comp, key,
                   {'text': cnt, 'lemma': ctx.lemmas[key]})
    return True


def ex_translit(key:Text, cnt:Text, comp:Text, ctx:cla_meta_intf):
    from sagas.nlu.transliterations import translits
    if translits.is_available_lang(ctx.lang):
        tval = translits.translit(cnt, ctx.lang)
        # tval=tval.replace('[UNK]', '').strip()
        ctx.add_result(extractor, comp, key, tval)
    else:
        ctx.add_result(extractor, comp, key, cnt)
    return True


def ex_dims(key:Text, cnt:Text, comp:Text, ctx:cla_meta_intf, dim):
    from sagas.nlu.inspectors import query_duckling
    resp = query_duckling(cnt, ctx.lang)
    # print('*************', cnt, ctx.lang, resp)
    values = [d for d in resp['data'] if d['dim'] == dim]
    if len(values) > 0:
        ctx.add_result(extractor, comp, key, values)
        return True
    return False


def ex_rasa(key:Text, cnt:Text, comp:Text, ctx:cla_meta_intf):
    from sagas.conf.conf import cf
    from sagas.nlu.rasa_procs import invoke_nlu

    endpoint = cf.ensure('nlu_multilang_servant')
    result = invoke_nlu(endpoint, ctx.lang, "current", ctx.sents)
    # print('*******', result)
    if result != None:
        ctx.add_result(extractor, comp, 'sents', result)
        return True
    return False


def ex_chunk(key:Text, cnt:Text, comp:Text, ctx:cla_meta_intf, clo):
    from sagas.nlu.uni_chunks import get_chunk
    from sagas.nlu.ruleset_procs import list_words, cached_chunks
    from sagas.conf.conf import cf
    # get_chunk(f'verb_domains', 'xcomp/obj', lambda w: w.upos)
    chunks = cached_chunks(ctx.sents, ctx.lang, cf.engine(ctx.lang))
    domain, path = key.split(':')
    result = get_chunk(chunks,
                       f'{domain}_domains' if domain != 'predicts' else domain,
                       path, clo=clo)
    logger.debug(f"extract chunk: {domain}, {path}, {result}")
    if len(result) > 0:
        ctx.add_result(extractor, comp, key, result)
        return True
    return False


def ex_feats(key:Text, cnt:Text, comp:Text, ctx:cla_meta_intf):
    from sagas.nlu.features import get_feats_map
    domain, path = key.split(':')
    result = get_feats_map(ctx.sents, ctx.lang, domain, path)
    if result:
        ctx.add_result(extractor, comp, key, result)
        return True
    return False


def ex_ner(key:Text, cnt:Text, comp:Text, ctx:cla_meta_intf):
    data = {"sents": ctx.sents if key == '_' else cnt}
    route = f'spacy/{ctx.lang}' if ctx.lang in ('zh', 'ru', 'ja', 'id') else ctx.lang
    response = requests.post(f'http://localhost:1700/ner/{route}', json=data)
    if response.status_code == 200:
        result = response.json()
        if result:
            ctx.add_result(extractor, comp, key, result)
            return True
    return False

class CompExtractInspector(Inspector):
    """
    提取指定成分:
    Instances:
        extract_for('chunk+chunk_text', 'verb:xcomp/obj'),
        nsubj=extract('plain+date_search+date_parse'),
        extract_for('feats', 'verb:_'),
        extract_for('feats', 'verb:obj')
    >>> pat(3, name='extract_day').cop(behaveof('day', 'n'),
    >>>                           flat=kindof('feast_day/day', 'n'),
    >>>                           nsubj=extract('plain+date_search+date_parse')),
    """
    def __init__(self, comp_as='plain', pickup=''):
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

        ex_map={'date_search': lambda cnt,comp: ex_date_search(key, cnt, comp, ctx),
                # .. extract_for('plain+date_search+date_parse', '時間'),
                'date_parse': lambda cnt,comp: ex_date_parse(key, cnt, comp, ctx),
                'plain': lambda cnt,comp: ex_plain(key, cnt, comp, ctx),
                'word': lambda cnt,comp: ex_word(key, cnt, comp, ctx),
                # .. extract_for('plain+translit', 'obj'),
                'translit': lambda cnt,comp: ex_translit(key, cnt, comp, ctx),
                'email': lambda cnt,comp: ex_dims(key, cnt, comp, ctx, 'email'),
                # .. extract_for('number', 'obl'),
                'number': lambda cnt, comp: ex_dims(key, cnt, comp, ctx,'number'),
                # .. extract_for('time', 'advmod'),
                'time': lambda cnt, comp: ex_dims(key, cnt, comp, ctx,'time'),
                # .. extract_for('plain+temperature', 'ニ'),
                'temperature': lambda cnt, comp: ex_dims(key, cnt, comp, ctx, 'temperature'),
                # example: extract_for('rasa', '_')
                'rasa': lambda cnt, comp: ex_rasa(key, cnt, comp, ctx),
                # example: extract_for('chunk', 'verb:xcomp/obj')
                'chunk': lambda cnt, comp: ex_chunk(key, cnt, comp, ctx, lambda w: (w.text, w.upos.lower())),
                # example: extract_for('chunk_text', 'verb:xcomp/obj')
                'chunk_text': lambda cnt, comp: ex_chunk(key, cnt, comp, ctx, lambda w: w.text),
                'chunk_feats': lambda cnt, comp: ex_chunk(key, cnt, comp, ctx, lambda w: w.feats),
                # .. extract_for('feats', 'verb:_'),
                #        extract_for('feats', 'verb:obj')
                'feats': lambda cnt, comp: ex_feats(key, cnt, comp, ctx),
                # example: extract_for('ner', '_'), extract_for('ner', 'xcomp')
                'ner': lambda cnt, comp: ex_ner(key, cnt, comp, ctx),
                }

        if self.pickup=='_' or is_full_domain_path(self.pickup):
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
    def when_succ(self):
        return True

    def __str__(self):
        return f"ins_{self.name()}({self.comp_as})"

extract=lambda c='plain': CompExtractInspector(c)
extract_dt=lambda c='plain+date_search+date_parse': CompExtractInspector(c)
extract_c=lambda p: CompExtractInspector('plain', p)
# extract_for('chunk+chunk_text', 'verb:xcomp/obj'),
extract_for=lambda f, p: CompExtractInspector(f, p)

