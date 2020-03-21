from typing import Text, Any, Dict, List, Union, Set
from blinker import NamedSignal, signal
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from sagas.conf.conf import cf
import sagas.tracker_fn as tc
from pprint import pprint
import logging

logger = logging.getLogger(__name__)

representers:List[Any]=[]

class ResultDataset(object):
    def __init__(self, results: List[Any]):
        self.dataset=results

@dataclass_json
@dataclass
class RequestMeta:
    sents: str
    lang: str
    engine: str

def process_tags_data(tags:Set[Text], results: List[Any], meta:Dict[Text,Any]):
    from sagas.nlu.signals import signals
    ds=ResultDataset(results)
    filter_keys={'sents', 'lang', 'engine'}
    req_meta=RequestMeta.from_dict({k:v for k,v in meta.items() if k in filter_keys})
    for tag in tags:
        resp = signals.fire('event_mediator', tag, dataset=ds, meta=req_meta)
        logger.debug(f"reps: {len(representers)}")
        for rep in representers:
            rep(req_meta, ds, resp)

class ConsoleRepresenter(object):
    def __call__(self, meta:RequestMeta, ds:ResultDataset, resp:List[Dict[Text, Any]]):
        # pprint(ds.dataset)
        for r in resp:
            print('******', r['name'], r['result'])

def init_reps():
    logger.debug('add console rep')
    representers.append(ConsoleRepresenter())


watch = signal('watch')
evts=[watch]

@watch.connect
def console_watch(sender, **kw):
    import datetime
    from sagas.nlu.nlu_tools import NluTools

    ds:ResultDataset=kw['dataset']
    meta:RequestMeta=kw['meta']

    print(f"****** watch {sender}")
    tc.emp('magenta', meta)

    tools = NluTools()
    if cf.is_enabled('print_tree'):
        tools.main_domains(meta.sents,
                           lang=meta.lang,
                           engine=meta.engine,
                           print_domains=False)

    return datetime.datetime.now()



