"""
See notebook: procs-dep-parser.ipynb
"""

def it(*dl):
    rs=[]
    for d in dl:
        rs.extend(d)
    return rs

def equals(a, b):
    return str(a) == str(b)

def head(word, sent):
    c=sent.words[word.governor - 1]
    return c

def children(word, sent):
    return filter(lambda w: equals(w.governor, word.index), sent.words)

def check_part_match(domain_list, **kwargs):
    rs=[]
    for k,v in kwargs.items():
        for domain in domain_list:
            rs.append(k in domain and domain[k]==v)
    return all(rs)

def check_fn(domain_list, meta, **kwargs):
    # print('.. domains size', len(domain_list))
    if len(domain_list) == 0:
        return False

    rs = []
    for k, v in kwargs.items():
        item_r = False
        for domain in domain_list:
            # 如果包含了该成分, 则这这个成分的测试值必须为真
            if k in domain and v(domain[k], meta):
                item_r = True
        # 如果domain_list里的所有元素都未包含该成分, 则会保留为false值
        rs.append(item_r)
    return all(rs) if len(rs)>0 else False

def predicate_fn(chain, pos):
    from sagas.nlu.inspector_wordnet import predicate
    return lambda word, meta: predicate(chain, word, meta["lang"], pos)

comp_rel=('flat', "compound", 'nmod', 'ccomp')
get_domains=lambda w,doc: [{pa.dependency_relation:pa.lemma} for pa in children(w, doc) if pa.dependency_relation not in comp_rel]

def anal(**kwargs):
    def perform(doc, meta):
        root = next(w for w in doc.words if w.dependency_relation in ('root', 'hed'))
        compounds=[w for w in children(root, doc) if w.dependency_relation in comp_rel]
        check_r=check_fn(it(*[get_domains(c,doc) for c in compounds]), meta, **kwargs)
        return check_r
    return perform



