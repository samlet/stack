from typing import Text, Any, Dict, List
from sagas.nlu.inspector_common import Inspector, Context
import logging

logger = logging.getLogger(__name__)


class TagsInspector(Inspector):
    def __init__(self, *tags):
        self.tags = tags

    def name(self):
        return "tags"

    def run(self, key, ctx: Context):
        ctx.add_result(self.name(), 'default', 'sents', list(self.tags))
        return True

    def when_succ(self):
        return True

    def __str__(self):
        return f"ins_{self.name()}({self.tags})"


