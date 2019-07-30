import sagas

def equals(a, b):
    return str(a) == str(b)

def get_children(sent, word, rs):
    for c in filter(lambda w: equals(w.governor, word.index), sent.words):
        rs.append((c.index, c.text))
        get_children(sent, c, rs)

def get_children_list(sent, word, include_self=True):
    rs = []
    get_children(sent, word, rs)
    if include_self:
        rs.append((word.index, word.text))
    # sort by word's index
    rs=sorted(rs, key=lambda _: int(_[0]))
    result = [w[1] for w in rs]
    # if include_self:
    #     result.append(word.text)
    return result

def get_word_features(word):
    # 'c' represent a chunk
    # return ['c_{}_{}'.format(word.lemma, word.upos).lower()]
    return ['c_{}'.format(word.upos).lower()]

def add_domain(domains, c, sent):
    domains.append((c.dependency_relation, c.index, c.text, c.lemma,
                    get_children_list(sent, c), get_word_features(c)))

def get_verb_domain(sent, filters):
    rs = []
    for word in filter(lambda w: w.upos == "VERB", sent.words):
        # if money.dep_ in ("attr", "dobj"):
        # print(word.index, word.text)
        domains = []
        for c in filter(lambda w: equals(w.governor, word.index), sent.words):
            # print('\t', c.index, c.text, get_children_list(sent, c))
            # domains.append((c.dependency_relation, c.index, c.text, c.lemma,
            #                 get_children_list(sent, c), get_word_features(c)))
            add_domain(domains, c, sent)
        rs.append({'type':'verb_domains', 'verb': word.text, 'index': word.index,
                   'domains': domains})
    return rs

def get_aux_domain(sent, filters):
    rs = []
    for word in filter(lambda w: w.upos == "AUX", sent.words):
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
        # 需要收集的是aux单词依赖的对象的关联集, 而不是aux单词自身的关联集
        for c in filter(lambda w: equals(w.governor, dc.index), sent.words):
            # print('\t', c.index, c.text, get_children_list(sent, c))
            # domains.append((c.dependency_relation, c.index, c.text, c.lemma,
            #                 get_children_list(sent, c), get_word_features(c)))
            add_domain(domains, c, sent)
        rs.append({'type':'aux_domains', 'aux': word.text,
                   'rel': word.dependency_relation, 'governor': word.governor, 'head': dc.text,
                   'head_pos': dc.upos.lower(), 'delegator':delegator,
                   'index': word.index, 'domains': domains})
    return rs

def get_subj_domain(sent):
    rs = []
    for word in filter(lambda w: w.dependency_relation.endswith('subj'), sent.words):
        dc=sent.words[word.governor-1]
        # print('℗', word.text, word.dependency_relation, word.governor, '☇' , dc.text)
        domains = []
        # 需要收集的是subj依赖的对象的关联集
        for c in filter(lambda w: equals(w.governor, dc.index), sent.words):
            # print('\t', c.index, c.text, get_children_list(sent, c))
            # domains.append((c.dependency_relation, c.index, c.text, c.lemma,
            #                 get_children_list(sent, c), get_word_features(c)))
            add_domain(domains, c, sent)
        rs.append({'type':'subj_domains', 'subj': word.text,
                   'rel': word.dependency_relation, 'governor': word.governor, 'head': dc.text,
                   'head_pos': dc.upos.lower(),
                   'index': word.index, 'domains': domains})
    return rs

class CoreNlpParser(object):
    def verb_domains(self, sents, lang='en'):
        """
        $ python -m sagas.nlu.corenlp_parser verb_domains "Barack Obama was born in Hawaii." en
        $ python -m sagas.nlu.corenlp_parser verb_domains 'Что ты обычно ешь на ужин?' ru
        $ python -m sagas.nlu.corenlp_parser verb_domains 'Die Zeitschrift erscheint monatlich.' de
        :param sents:
        :param lang:
        :return:
        """
        from sagas.nlu.corenlp_helper import CoreNlp, CoreNlpViz, get_nlp
        nlp = get_nlp(lang)
        doc=nlp(sents)
        # 分析依赖关系, 自下而上, 可用于抽取指定关系的子节点集合, 比如此例中的'nsubj:pass'和'obl'
        # word.governor即为当前word的parent
        sent = doc.sentences[0]
        r = get_verb_domain(sent, ['obl', 'nsubj:pass'])
        # print(json.dumps(r, indent=2, ensure_ascii=False))
        print(r[0]['verb'], r[0]['index'])
        df=sagas.to_df(r[0]['domains'], ['rel', 'index', 'text', 'children'])
        sagas.print_df(df)

if __name__ == '__main__':
    import fire
    fire.Fire(CoreNlpParser)