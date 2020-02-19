import sagas
import logging

logger = logging.getLogger(__name__)

def equals(a, b):
    return str(a) == str(b)

# except_from_stems=['DET']
def get_children(sent, word, rs, stem):
    for c in filter(lambda w: equals(w.governor, word.index), sent.words):
        rs.append((c.index, c.lemma if stem else c.text))
        get_children(sent, c, rs, stem)

def get_children_index(sent, word):
    rs = []
    get_children(sent, word, rs, stem=False)
    return [word.index]+[w[0] for w in rs]

def get_children_list(sent, word, include_self=True, stem=False):
    rs = []
    get_children(sent, word, rs, stem)
    if include_self:
        rs.append((word.index, word.lemma if stem else word.text))
    # sort by word's index
    rs=sorted(rs, key=lambda _: int(_[0]))
    result = [w[1] for w in rs]
    # if include_self:
    #     result.append(word.text)
    return result

def get_word_features(word):
    # 'c' represent a chunk
    # return ['c_{}_{}'.format(word.lemma, word.upos).lower()]
    feats=[]
    feats.append('c_{}'.format(word.upos).lower())
    if word.xpos!='_':
        feats.append('x_{}'.format(word.xpos).lower())
    return feats

def add_domain(domains:list, stems:list,  c, sent):
    domains.append((c.dependency_relation, c.index, c.text, c.lemma,
                    get_children_list(sent, c), get_word_features(c)))
    stems.append((c.dependency_relation, get_children_list(sent, c, include_self=True, stem=True)))

def add_head(domains:list, word, sent):
    if word.governor!=0:
        c=sent.words[word.governor - 1]
        domains.append((f"head_{word.dependency_relation}",
                        c.index, c.text, c.lemma,
                        [c.text], get_word_features(c)))

def get_verb_domain(sent):
    from sagas.nlu.uni_intf import sub_comps
    rs = []
    verbs=list(filter(lambda w: w.upos == "VERB", sent.words))
    if len(verbs)>1:
        # filter the verbs which in clausal complement
        verbs=[word for word in verbs if word.dependency_relation not in sub_comps]
    for word in verbs:
        # if money.dep_ in ("attr", "dobj"):
        # print(word.index, word.text)
        domains = []
        stems=[]
        for c in filter(lambda w: equals(w.governor, word.index), sent.words):
            # print('\t', c.index, c.text, get_children_list(sent, c))
            # domains.append((c.dependency_relation, c.index, c.text, c.lemma,
            #                 get_children_list(sent, c), get_word_features(c)))
            add_domain(domains, stems, c, sent)

        # add governor as head domain
        # add_domain(domains, stems, sent.words[word.governor - 1], sent)
        add_head(domains, word, sent)

        rs.append({'type':'verb_domains', 'word': word.text, 'lemma':word.lemma, 'index': word.index,
                   'upos': word.upos.lower(), 'xpos': word.xpos.lower(),
                   'rel': word.dependency_relation, 'governor': word.governor,
                   'domains': domains, 'stems':stems})
    return rs

def get_aux_domain(sent):
    rs = []
    parsed_heads=set()
    for word in filter(lambda w: w.upos == "AUX", sent.words):
        if word.governor in parsed_heads:
            continue

        # dc=sent.words[word.governor-1]
        if word.governor == 0:
            # if the aux word is root; (这种情形会出现在德语依存分析中, 但在英语依存分析中是正常的)
            dc = word
            delegator=True
        else:
            dc = sent.words[word.governor - 1]
            delegator=False
        # print('℗', word.text, word.dependency_relation, word.governor, '☇' , dc.text)
        # print('\t', dc.index, dc.text, get_children_list(sent, dc))
        domains = []
        stems = []
        # 需要收集的是aux单词依赖的对象的关联集, 而不是aux单词自身的关联集
        for c in filter(lambda w: equals(w.governor, dc.index), sent.words):
            # print('\t', c.index, c.text, get_children_list(sent, c))
            # domains.append((c.dependency_relation, c.index, c.text, c.lemma,
            #                 get_children_list(sent, c), get_word_features(c)))
            add_domain(domains, stems, c, sent)

        add_head(domains, dc, sent)
        rs.append({'type':'aux_domains', 'word': word.text, 'lemma':word.lemma,
                   'rel': word.dependency_relation, 'governor': word.governor,
                   # 'head': dc.text,
                   'head': dc.lemma,
                   'head_pos': dc.upos.lower(), 'delegator':delegator,
                   'index': word.index, 'domains': domains, 'stems':stems})
        parsed_heads.add(word.governor)
    return rs

def get_subj_domain(sent):
    rs = []
    for word in filter(lambda w: w.dependency_relation.endswith('subj'), sent.words):
        dc=sent.words[word.governor-1]
        # print('℗', word.text, word.dependency_relation, word.governor, '☇' , dc.text)
        domains = []
        stems = []
        # 需要收集的是subj依赖的对象的关联集
        for c in filter(lambda w: equals(w.governor, dc.index), sent.words):
            # print('\t', c.index, c.text, get_children_list(sent, c))
            # domains.append((c.dependency_relation, c.index, c.text, c.lemma,
            #                 get_children_list(sent, c), get_word_features(c)))
            add_domain(domains, stems, c, sent)

        add_head(domains, dc, sent)
        rs.append({'type':'subj_domains', 'word': word.text, 'lemma':word.lemma,
                   'rel': word.dependency_relation, 'governor': word.governor,
                   'head': dc.lemma,
                   'head_pos': dc.upos.lower(), 'head_feats':[dc.lemma, dc.upos, dc.xpos],
                   'index': word.index, 'domains': domains, 'stems':stems})
    return rs

def get_root_domain(sent_p):
    root = next(w for w in sent_p.words if w.dependency_relation in ('root', 'hed'))
    logging.debug(f"root: {root.index}, {root.text}({root.upos})")
    root_idx = int(root.index)
    domains = []
    stems = []
    rs = []
    for word in (w for w in sent_p.words if w.governor == root_idx):
        # print(f"{__name__}: {word.dependency_relation}: {word.text}")
        logging.debug(f"{word.dependency_relation}: {word.text}")
        add_domain(domains, stems, word, sent_p)

    word = root
    rs.append({'type': 'root_domains', 'word': word.text, 'lemma': word.lemma,
               'upos': word.upos.lower(), 'xpos': word.xpos.lower(),
               'rel': word.dependency_relation, 'governor': word.governor,
               'index': word.index, 'domains': domains, 'stems': stems})
    return rs

domain_getters={"verb": get_verb_domain,
                'aux': get_aux_domain,
                'subj': get_subj_domain,
                'root': get_root_domain,
                }
def get_chunks(sent, return_root_chunks_if_absent=True, specified=None):
    if specified is not None:
        return domain_getters[specified](sent)

    r = get_verb_domain(sent)
    if len(r) == 0:
        r = get_aux_domain(sent)
    if len(r) == 0:
        r = get_subj_domain(sent)
    if len(r)==0 and return_root_chunks_if_absent:
        r=get_root_domain(sent)
    return r

class CoreNlpParser(object):
    def verb_domains(self, sents, lang='en'):
        """
        $ python -m sagas.nlu.corenlp_parser verb_domains "Barack Obama was born in Hawaii." en
        # 我有一只阿比西尼亚猫
        $ python -m sagas.nlu.corenlp_parser verb_domains "I have an Abyssinian cat." en

        $ python -m sagas.nlu.corenlp_parser verb_domains 'Что ты обычно ешь на ужин?' ru
        $ python -m sagas.nlu.corenlp_parser verb_domains 'Die Zeitschrift erscheint monatlich.' de

        # 测试多个动词(过滤掉从句的动词):
        $ python -m sagas.nlu.corenlp_parser verb_domains 'Tu as choisi laquelle tu vas manger ?' fr
        :param sents:
        :param lang:
        :return:
        """
        from sagas.nlu.corenlp_helper import CoreNlp, CoreNlpViz, get_nlp
        serial_numbers = '❶❷❸❹❺❻❼❽❾❿'
        nlp = get_nlp(lang)
        doc=nlp(sents)
        # 分析依赖关系, 自下而上, 可用于抽取指定关系的子节点集合, 比如此例中的'nsubj:pass'和'obl'
        # word.governor即为当前word的parent
        sent = doc.sentences[0]
        rs = get_verb_domain(sent)
        # r=rs[0]
        for num, r in enumerate(rs):
            # print(json.dumps(r, indent=2, ensure_ascii=False))
            print(serial_numbers[num], '-'*50)
            # print(r['verb'], r['index'])
            print(r['word'], r['index'])
            # df=sagas.to_df(r[0]['domains'], ['rel', 'index', 'text', 'children'])
            df = sagas.to_df(r['domains'], ['rel', 'index', 'text', 'lemma', 'children', 'features'])
            sagas.print_df(df)
            for stem in r['stems']:
                if stem[0]=='obj':
                    print('object ->', ' '.join(stem[1]))

if __name__ == '__main__':
    import fire
    fire.Fire(CoreNlpParser)