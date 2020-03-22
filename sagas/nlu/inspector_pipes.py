from typing import Text, Any, Dict, List, Union
from sagas.nlu.inspector_common import Context, Inspector

from blinker import NamedSignal, signal
import rx
from rx import operators as ops
from dataclasses import dataclass
from sagas.util.collection_util import to_obj
import logging
logger = logging.getLogger(__name__)


@dataclass
class token_data:
    word: str
    pos: str
    path: str

def filter_pos(pos_list:List[Text]):
    return rx.pipe(
        ops.filter(lambda t: t.upos.lower() in pos_list),
    )
def to_token():
    return rx.pipe(
        ops.map(lambda t: token_data(word=f"{t.text}/{t.lemma}",
                                     path=t.path,
                                     pos=t.upos.lower())),)

collect = signal('collect')
@collect.connect
def collect_pos(sender, **kwargs):
    results=[]
    source = rx.of(*kwargs['rs'])
    pos_list:List[Text]=kwargs['data']
    source.pipe(
        filter_pos(pos_list),
        to_token(),
    ).subscribe(
        on_next=lambda value: results.append(value),
        on_error=lambda e: print(e),
        on_completed=lambda: print("done."),
    )
    return results

def flat_table(ds, parent, table_rs):
    child_tags=[k for k,v in ds.items() if isinstance(v, list) and k not in ('entity', 'segments')]
    path=f"{parent}/{ds['dependency_relation']}"
    data={}
    for k,v in ds.items():
        if k in child_tags:
            for vchild in v:
                flat_table(vchild, path, table_rs)
        else:
            data[k]=v
    table_rs.append(to_obj({'path':path, **data}))

class PipesInspector(Inspector):
    """
    Pipes inspector
    Instances: pipes(collect=['verb']),
    """
    def __init__(self, **kwargs):
        self.parameters=kwargs
        self.sigs_conf=[(signal(sig), paras) for sig,paras in kwargs.items()]

    def name(self):
        return "pipes"

    def get_domains(self, ctx:Context):
        from sagas.nlu.ruleset_procs import cached_chunks
        from sagas.conf.conf import cf

        # dn = lambda domain: f'{domain}_domains' if domain != 'predicts' else domain
        chunks = cached_chunks(ctx.sents, ctx.lang, cf.engine(ctx.lang))
        domains = chunks[ctx.domain_type]
        return domains

    def process_result(self, ctx:Context, results:List[Dict[Text, Any]]) -> bool:
        """
        Results sample:
        [{'name': 'collect_verb',
            'result': [token_data(word='think/think', pos='verb', path='/root')]}]
        :param results:
        :return:
        """
        for result in results:
            logger.debug(result)
            ctx.add_result(self.name(),
                           provider=result['sig'],
                           part_name=result['name'],
                           val=result['result'])
        return True

    def run(self, key, ctx:Context):
        # see also: procs-inspector-pipes.ipynb

        table_rs = []
        domains=self.get_domains(ctx)
        for ds in domains:
            flat_table(ds, '', table_rs)

        results = []
        for sig, paras in self.sigs_conf:
            result = sig.send(self.name(), rs=table_rs, data=paras)
            if result:
                results.extend([{'name': fn.__name__, 'sig':sig.name, 'result': r} for fn, r in result])
        if results:
            return self.process_result(ctx, results)
        else:
            return False

    def __str__(self):
        return f"ins_{self.name()}({self.parameters})"


