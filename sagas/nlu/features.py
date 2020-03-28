from jsonpath_ng import jsonpath, parse
from pprint import pprint
from sagas.conf.conf import cf

def feats_for_path(path):
    if path=='_':
        return '$.feats'
    prefix = '$.'
    suffix = '.feats'
    parts = path.split('/')
    parts_str = '.'.join([f"{t}[*]" for t in parts])
    return f"{prefix}{parts_str}{suffix}"

def feats_map(ft):
    tuples=[pairs.split('=') for pairs in ft.split('|')]
    ft_m={k:v for k,v in tuples}
    return ft_m

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

