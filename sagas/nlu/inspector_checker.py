from typing import Text, Any, Dict, List
from sagas.nlu.inspector_common import Inspector, Context
import logging

logger = logging.getLogger(__name__)

class CheckerInspector(Inspector):
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
        def nagative(part):
            from sagas.nlu.inspectors_dataset import nagative_maps
            data_map = nagative_maps[ctx.lang]
            return check(data_map, 'negative')
        checkers={'has_rel': lambda c: c in ctx.rels,
                  'has_pos': lambda pos_list: ctx.pos in pos_list,
                  'has_lemma': lambda ls: has_lemma(ls),
                  'negative': lambda part: nagative(part),
                  }
        results=[]
        for para,val in self.paras.items():
            results.append(checkers[para](val))
        return all(results)

    def __str__(self):
        return f"ins_{self.name()}{self.paras}"

