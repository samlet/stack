meta_pickups={
    'aux_domains': lambda r, common, data: {'pos': r['head_pos'], 'head': r['head'], **common, **data},
    'root_domains': lambda r, common, data: {'rel': r['rel'], **common, **data},
    'verb_domains': lambda r, common, data: {'rel': r['rel'], **common, **data},
    'predicate': lambda r, common, data: {'pos': r['pos'], 'rel': r['rel'], **common, **data},
    'subj_domains': lambda r, common, data: {'pos': r['head_pos'], 'head': r['head'], **common, **data},
}

def build_meta(r, data):
    type_name = r['type']
    common = {'lemma': r['lemma'], 'word': r['word'],
              'stems': r['stems']}

    if type_name in meta_pickups:
        return meta_pickups[type_name](r, common, data)
    else:
        return {'rel': r['rel'], **common, **data}

