from typing import Text, Any, Dict, List, Set
from sagas.nlu.inspector_common import Inspector, Context
from sagas.nlu.registries import sinkers_fn
import logging

logger = logging.getLogger(__name__)

class InferencerInspector(Inspector):
    def __init__(self, *tools):
        self.tools = tools

    def name(self):
        return "infer"

    def infer(self, insps:List, insp_pairs:Dict[Text, Any]):
        logger.debug(str({t.__name__ for t in insps}))
        logger.debug(str({k:t.__name__ for k,t in insp_pairs.items()}))

    def run(self, key, ctx: Context):
        ctx.add_result(self.name(), 'default', 'defined', list(self.tools))
        return True

    def when_succ(self):
        return True

    def __str__(self):
        # names={t.__name__ for t in self.tools}
        return f"ins_{self.name()}({self.tools})"

