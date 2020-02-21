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
        checkers={'has_rel': lambda c: c in ctx.rels,
                  'has_pos': lambda pos_list: ctx.pos in pos_list,
                  }
        results=[]
        for para,val in self.paras.items():
            results.append(checkers[para](val))
        return all(results)

    def __str__(self):
        return f"ins_{self.name()}{self.paras}"

