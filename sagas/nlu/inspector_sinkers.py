from typing import Text, Any, Dict, List
from sagas.nlu.inspector_common import Inspector, Context
from sagas.nlu.sinkers import sinkers_fn
import logging

logger = logging.getLogger(__name__)


def tags(results: List[Any]):
    val_list = [r['value'] for r in results if r['inspector'] == 'tags']
    all_tags = set([item for sublist in val_list for item in sublist])

    logger.info(f"tags: {all_tags}")

sinkers_fn.append(tags)

class TagsInspector(Inspector):
    """
    Instances: tags('age?')
    """
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


