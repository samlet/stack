from typing import Text, Any, Dict, List, Set
from sagas.nlu.inspector_common import Inspector, Context
from sagas.nlu.registries import sinkers_fn
import logging

logger = logging.getLogger(__name__)


def get_all_tags(results: List[Any]) -> Set[Text]:
    val_list = [r['value'] for r in results if r['inspector'] == 'tags']
    all_tags = set([item for sublist in val_list for item in sublist])
    return all_tags

def _tags(results: List[Any], data:Dict[Text,Any]):
    all_tags=get_all_tags(results)
    if all_tags:
        from sagas.nlu.sinker_orm import post_sents
        logger.info(f"tags: {all_tags}")
        post_sents(data['sents'], data['lang'], list(all_tags))

sinkers_fn.append(_tags)

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


class KeyValuesInspector(Inspector):
    def __init__(self, provider, **kwargs):
        self.provider=provider
        self.fields=kwargs

    def run(self, key, ctx: Context):
        ctx.add_result(self.name(), self.provider, 'defined', self.fields)
        return True

    def when_succ(self):
        return True

    def __str__(self):
        return f"ins_{self.name()}({self.fields})"


class SeriesInspector(KeyValuesInspector):
    def name(self):
        return "series"

class SlotsInspector(KeyValuesInspector):
    def name(self):
        return "slots"

