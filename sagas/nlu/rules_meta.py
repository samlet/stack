meta_pickups={
    'aux_domains': lambda r, common, data: {
        'pos': r['head_pos'], 'head': r['head'], 'head_word': r['head_word'],
        **common, **data},
    'root_domains': lambda r, common, data: {'pos': r['upos'], 'rel': r['rel'], **common, **data},
    'verb_domains': lambda r, common, data: {'pos': r['upos'], 'rel': r['rel'], **common, **data},
    'predicate': lambda r, common, data: {
        'pos': r['pos'], 'rel': r['rel'],
        'segments':r['segments'] if 'segments' in r else [],
        **common, **data},
    'subj_domains': lambda r, common, data: {
        'pos': r['head_pos'], 'head': r['head'], 'head_word': r['head_word'],
        **common, **data},
}

def build_meta(r, data):
    # from sagas.conf.conf import cf

    type_name = r['type']
    common = {'lemma': r['lemma'], 'word': r['word'], 'index': r['index'],
              'stems': r['stems']}
    # if 'engine' not in data:
    #     data['engine']=cf.engine(data['lang'])

    if type_name in meta_pickups:
        return meta_pickups[type_name](r, common, data)
    else:
        return {'rel': r['rel'], **common, **data}

