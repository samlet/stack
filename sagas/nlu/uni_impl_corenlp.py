from sagas.nlu.uni_intf import WordIntf, SentenceIntf

class CoreNlpWordImpl(WordIntf):
    def setup(self, data):
        features = ['index', 'text', 'lemma', 'upos', 'xpos',
                    'feats', 'governor', 'dependency_relation']
        attrs = {k: getattr(data, k) for k in features if getattr(data, k) is not None}
        return attrs


class CoreNlpSentImpl(SentenceIntf):
    def setup(self, sent):
        words = []
        for word in sent.words:
            words.append(CoreNlpWordImpl(word))
        deps = []
        for dep in sent.dependencies:
            # (governor, word.dependency_relation, word)
            deps.append((CoreNlpWordImpl(dep[0]), dep[1], CoreNlpWordImpl(dep[2])))
        return words, deps


class CoreNlpParserImpl(object):
    def __init__(self, lang):
        self.lang = lang

    def __call__(self, sents):
        from sagas.nlu.corenlp_helper import get_nlp
        nlp = get_nlp(self.lang)
        doc = nlp(sents)
        return CoreNlpSentImpl(doc.sentences[0])
