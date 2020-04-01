from typing import Text, Any, Dict, List, Set, Union, Optional
from dataclasses import dataclass
from sagas.nlu.inspector_common import Inspector, Context
from sagas.nlu.inspectors import NamedArgInspector
from sagas.nlu.registries import registry_sinkers, named_exprs
from sagas.conf.conf import cf
import logging
import sagas.tracker_fn as tc
from pprint import pprint

logger = logging.getLogger(__name__)

def get_all_tags(results: List[Any]) -> Set[Text]:
    val_list = [r['value'] for r in results if r['inspector'] == 'tags']
    all_tags = set([item for sublist in val_list for item in sublist])
    return all_tags

def _tags(results: List[Any], data:Dict[Text,Any]):
    all_tags=get_all_tags(results)
    if all_tags:
        from sagas.nlu.sinker_orm import post_sents
        from sagas.nlu.events import process_tags_data

        logger.info(f"tags: {all_tags}")
        post_sents(data['sents'], data['lang'], list(all_tags))
        process_tags_data(all_tags, results, data)

def _series(results: List[Any], data:Dict[Text,Any]):
    from jsonpath_ng import jsonpath, parse
    # val_list = [r['value'] for r in results if r['inspector'] == 'series']
    series_ins = [r for r in results if r['inspector'] == 'series']

    for series in series_ins:
        # print(f"{val}")
        val=series['value']
        tags = {}
        fields = {}
        for k, expr in val.items():
            if k.startswith('_'):
                key = k[1:]
                target_c = fields
            else:
                key = k
                target_c = tags
            ins_name, val_expr = expr.split(':')
            head = next(item for item in results if item['inspector'] == ins_name)
            vals = head['value']
            if val_expr.startswith('$'):
                jsonpath_expr = parse(val_expr)
                eval_val = next(match.value for match in jsonpath_expr.find(vals))
            else:
                eval_val = vals[val_expr]
            target_c[key] = eval_val

        # post series data
        from sagas.nlu.sinker_series import series_store
        series_store.post(series['provider'], tags, fields)
        logger.info(f"post to {series['provider']}: {tags}; {fields}")

def _slots(results: List[Any], data:Dict[Text,Any]):
    from sagas.nlu.sinker_cache import cache_store
    from sagas.nlu.sinker_rasa_tracker import rasa_tracker_store
    slots_ins = [r for r in results if r['inspector'] == 'slots']
    driver_fire={'cache': lambda bucket,vals: cache_store.store(bucket, vals),
                 'tracker': lambda bucket, vals: rasa_tracker_store.store(bucket, vals),
                 }
    for slots in slots_ins:
        fn=slots['value']['fn']
        drivers = slots['value']['driver'].split('+')
        for f in fn.split(','):
            r = named_exprs[f.strip()](results)
            value_map=dict(zip(*r))
            bucket=slots['provider']
            logger.info(f"post slots to {bucket}, drivers is {drivers}: {value_map}")
            # cache_store.store(bucket, value_map)
            for driver in drivers:
                driver_fire[driver](bucket, value_map)

def _dev_info(results: List[Any], data:Dict[Text,Any]):
    if cf.is_enabled('print_detail'):
        if results:
            pprint(results)
        else:
            print('.. no results')

def _descriptors(results: List[Any], data:Dict[Text,Any]):
    from sagas.nlu.descriptor import Descriptor
    logger.debug(f"data keys: {list(data.keys())}")
    dsp = Descriptor()
    pats=dsp.build(results)
    tc.emp('cyan', f"✁ render patterns {len(pats)}. {'-' * 25}")
    for i,pat in enumerate(pats.values()):
        tc.emp('magenta', f"{i}. {pat}")

    if cf.is_enabled('print_detail'):
        pprint(list(dsp.value_map.values()) or '.. no rendered results')

registry_sinkers(_tags, _series, _slots, _dev_info, _descriptors)

class TagsInspector(Inspector):
    """
    Instances:
        tags('age?'),
        tags('inform'),
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

    @property
    def result_map(self):
        return {}

    def run(self, key, ctx: Context):
        self.fields.update(self.result_map)
        ctx.add_result(self.name(), self.provider, 'defined',self.fields)
        return True

    def when_succ(self):
        return True

    def __str__(self):
        return f"ins_{self.name()}({self.fields})"


class SeriesInspector(KeyValuesInspector):
    """
    Instances:
        series('events',
                action='specs_of:category',
                object='kind_of:category',
                _count='ins_date:$[0].value.value'),
    Testcases: $ sj '流しを8つ直した。'
    """
    def name(self):
        return "series"

class SlotsInspector(KeyValuesInspector):
    """
    Instances:
        slots('transport', fn='from_to,transport'),
        slots('transport', fn='from_to,transport', driver='cache+tracker'),
    Testcases: $ sj '新幹線で東京から大阪まで行きました。'
    Notes: 如果使用tracker作为driver, 需要先将相应的slots名称添加到rasa-domain中
    """

    def __init__(self, provider, **kwargs):
        super().__init__(provider, **kwargs)
        self.driver=kwargs['driver'] if 'driver' in kwargs else 'cache'

    def name(self):
        return "slots"

    @property
    def result_map(self):
        return {'driver':self.driver}

class FactsInspector(NamedArgInspector):
    """
    >>> facts=FactsInspector
    >>> fact('/obj').is_cat('person').with_roles(x='len').into(facts)
    """
    pass


@dataclass
class fact:
    part: str
    roles: Optional[Dict]
    cat: Optional[str]

    def __init__(self, part):
        self.part = part
        self.roles = {}
        self.cat = ''

    def is_cat(self, cat):
        self.cat = cat
        return self

    def with_roles(self, **roles):
        self.roles = roles
        return self

    def into(self, ins):
        return ins(self)

