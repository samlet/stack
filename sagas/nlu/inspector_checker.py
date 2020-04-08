from typing import Text, Any, Dict, List, Union
from sagas.nlu.inspector_common import Inspector, Context
import logging

logger = logging.getLogger(__name__)

class CheckerInspector(Inspector):
    """
    Instances: checker(has_lemma='ない'),
        checker(negative='_'),
        checker(has_rel='ニクラベル'),
        checker(has_num='verb:obj'),
        checker(has_all_rels=['カラ', 'マデ']),

    >>> pat(3, name='obj_num').verb(checker(has_num='verb:obj'), ),
    """
    def __init__(self, **kwargs):
        self.paras=kwargs

    def name(self):
        return "checker"

    def run(self, key, ctx:Context):
        def check(lemmas, checker_name:Text):
            for lemma in lemmas:
                succ, _=ctx.in_segments(lemma)
                if succ:
                    ctx.add_result(self.name(), checker_name, 'predicate', lemmas)
                    return True
            return False
        def has_lemma(lemmas):
            if isinstance(lemmas, str):
                lemmas=[lemmas]
            return check(lemmas, 'has_lemma')
        def negative(part='_'):
            from sagas.nlu.inspectors_dataset import negative_maps
            data_map = negative_maps[ctx.lang]
            return check(data_map, 'negative')
        def has_pos_in_part(part:Text, pos: Union[list, str]):
            from sagas.nlu.uni_chunks import get_chunk
            from sagas.nlu.ruleset_procs import list_words, cached_chunks
            from sagas.conf.conf import cf
            chunks = cached_chunks(ctx.sents, ctx.lang, cf.engine(ctx.lang))
            domain,path = part.split(':')
            result = get_chunk(chunks,
                               f'{domain}_domains' if domain!='predicts' else domain,
                               path, lambda w: (w.upos.lower(), w.text))
            if isinstance(pos, str):
                pos=[pos]
            succ=False
            for el in result:
                if el[0] in pos:
                    ctx.add_result(self.name(), f'has_pos_{"_or_".join(pos)}', part, el[1])
                    succ=True
            return succ
        checkers={'has_rel': lambda c: c in ctx.rels,
                  'has_any_rels': lambda c: any(elem in ctx.rels for elem in c),
                  'has_all_rels': lambda c: all(elem in ctx.rels for elem in c),
                  'has_pos': lambda pos_list: ctx.pos in pos_list,
                  'has_lemma': lambda ls: has_lemma(ls),
                  'negative': lambda part: negative(part),
                  'has_num': lambda part: has_pos_in_part(part, 'num'),
                  }
        results=[]
        for para,val in self.paras.items():
            results.append(checkers[para](val))
        return all(results)

    def __str__(self):
        return f"ins_{self.name()}{self.paras}"

