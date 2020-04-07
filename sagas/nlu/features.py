from typing import Text, Any, Dict, List, Union, Optional
from jsonpath_ng import jsonpath, parse
from pprint import pprint
from sagas.conf.conf import cf

def feats_for_path(path:Text):
    if path=='_':
        return '$.feats'
    prefix = '$.'
    suffix = '.feats'
    parts = path.split('/')
    parts_str = '.'.join([f"{t}[*]" for t in parts])
    return f"{prefix}{parts_str}{suffix}"

def feats_map(ft:Text) -> Dict[Text, Text]:
    if not ft:
        return {}

    def ensure(pair):
        p=pair.split('=')
        return (p[0],'_') if len(p)==1 else p
    tuples=[ensure(pair) for pair in ft.split('|')]
    ft_m={k:v for k,v in tuples}
    return ft_m

def extract_feats_map(ft:Text, engine:Text) -> Dict[Text, Text]:
    ex_fn={'corenlp': feats_map,
           'stanza': feats_map}
    engine=engine.split('_')[0]
    if engine in ex_fn:
        return ex_fn[engine](ft)
    return {}

def get_feats_map(sents, lang, domain, path):
    domain_name=f'{domain}_domains' if domain != 'predicts' else domain
    from sagas.nlu.ruleset_procs import cached_chunks
    chunks = cached_chunks(sents, lang, cf.engine(lang))
    parser = parse(feats_for_path(path))
    results=[]
    for chunk in chunks[domain_name]:
        vals = [match.value for match in parser.find(chunk)]
        if vals:
            results.extend([feats_map(val) for val in vals])
    return results

