meta_pickups={
    'aux_domains': lambda r, common, data: {'pos': r['head_pos'], 'head': r['head'], **common, **data},
    'root_domains': lambda r, common, data: {'rel': r['rel'], **common, **data},
    'verb_domains': lambda r, common, data: {'rel': r['rel'], **common, **data},
    'subj_domains': lambda r, common, data: {'pos': r['head_pos'], 'head': r['head'], **common, **data},
}

def build_meta(r, common, data):
    type_name = r['type']
    if type_name in meta_pickups:
        return meta_pickups[type_name](r, common, data)
    else:
        return {'rel': r['rel'], **common, **data}

