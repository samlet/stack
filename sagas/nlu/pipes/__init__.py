from typing import Text, Any, Dict, List, Union, Optional
from rx import Observable
from dataclasses import dataclass
from sagas.util.collection_util import to_obj
import rx
from rx import operators as ops
from sagas.util.collection_util import wrap

@dataclass
class pred_cond:
    part: str
    cond: Union[Text, List[Text]]

@dataclass
class sense_cond:
    part: str
    roles: Optional[Dict]
    cat: Optional[str]

    @staticmethod
    def is_cat(part, cat):
        return sense_cond(part, None, cat)

    @staticmethod
    def has_roles(part, **roles):
        return sense_cond(part, roles, None)
    def with_roles(self, **roles):
        self.roles=roles
        return self

def filter_path(*cands):
    return rx.pipe(
        ops.filter(lambda t: t.path in cands),)

def filter_pos(pos_list:List[Text]):
    return rx.pipe(
        ops.filter(lambda t: t.upos.lower() in pos_list),
    )

def to_token(value=''):
    return rx.pipe(
        ops.map(lambda t: wrap(word=f"{t.text}/{t.lemma}",
                               path=t.path,
                               pos=t.upos.lower(),
                               value=value)), )

def flat_table(ds, parent, table_rs, is_root=True):
    child_tags=[k for k,v in ds.items() if isinstance(v, list) and k not in ('entity', 'segments')]
    path=f"{parent}/{ds['dependency_relation']}" if not is_root else ''
    data={}
    for k,v in ds.items():
        if k in child_tags:
            for vchild in v:
                flat_table(vchild, path, table_rs, is_root=False)
        else:
            data[k]=v
    table_rs.append(to_obj({'path':path, **data}))

def get_source(sents, lang, domain_type=None)-> Observable:
    from sagas.nlu.ruleset_procs import cached_chunks, get_main_domains
    from sagas.conf.conf import cf
    import rx

    engine=cf.engine(lang)
    if domain_type is None:
        domain_type, domains=get_main_domains(sents, lang, engine)
    else:
        chunks = cached_chunks(sents, lang, engine)
        domains = chunks[domain_type]
    table_rs = []
    for ds in domains:
        flat_table(ds, '', table_rs)
    return rx.of(*table_rs)


# __all__=['helpers']
from . import pos, collect, interrogative, cat, sense


