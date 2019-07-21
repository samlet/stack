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
    result = [w[1] for w in rs]
    if include_self:
        result.append(word.text)
    return result

def get_verb_domain(sent, filters):
    rs = []
    for word in filter(lambda w: w.upos == "VERB", sent.words):
        # if money.dep_ in ("attr", "dobj"):
        # print(word.index, word.text)
        domains = []
        for c in filter(lambda w: equals(w.governor, word.index), sent.words):
            # print('\t', c.index, c.text, get_children_list(sent, c))
            domains.append((c.dependency_relation, c.index, c.text, get_children_list(sent, c)))
        rs.append({'verb': word.text, 'index': word.index, 'domains': domains})
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