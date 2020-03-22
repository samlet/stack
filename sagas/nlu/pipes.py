from rx import Observable

from sagas.util.collection_util import to_obj

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

