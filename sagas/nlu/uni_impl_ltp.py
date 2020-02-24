from typing import Text, Any, Dict, List
from sagas.nlu.uni_intf import RootWordImpl, WordIntf, SentenceIntf

upos_maps={'a':'ADJ', 'p':'ADP', 'd':'ADV',
           'u':'AUX', 'c':'CCONJ', 'h':'DET',
           'e':'INTJ', 'n':'NOUN', 'm':'NUM',
           'z':'PART', 'r':'PRON', 'nh':'PROPN',
           'wp':'PUNCT', 'ws':'SYM',
           'v':'VERB', 'x':'X'
          }
upos_rev_maps={'SCONJ':['c'], 'NOUN':['ni', 'nl', 'ns', 'nt', 'nz', 'n', 'nd', 'nh']}

def get_pos_mapping(pos, default_val='X'):
    if pos in upos_maps:
        return upos_maps[pos]
    else:
        for k, v in upos_rev_maps.items():
            if pos in v:
                return k
    return default_val

class WordUnit(object):
    def __init__(self, i, text, dependency_relation, governor, head_text, pos, netag):
        self.i=i
        self.text=text
        self.lemma=text
        self.dependency_relation=dependency_relation
        self.governor=governor
        self.head_text=head_text
        self.pos=pos
        self.upos=get_pos_mapping(pos)

        self.netag=netag


class LtpWordImpl(WordIntf):
    def setup(self, token):
        if token.dependency_relation == 'HED':
            governor = 0
            rel='root'
        else:
            governor = token.governor
            rel=token.dependency_relation.lower()
        idx = token.i + 1  # start from 1
        features = {'index': idx, 'text': token.text, 'lemma': token.lemma,
                    'upos': token.upos, 'xpos': token.pos,
                    'feats': [], 'governor': int(governor), 'dependency_relation': rel,
                    'entity': [token.netag]
                    }
        return features


class LtpSentImpl(SentenceIntf):
    def __init__(self, sent, text, predicts=None):
        super().__init__(sent, text, predicts)

    def setup(self, sent):
        words = []
        for word in sent:
            words.append(LtpWordImpl(word))
        deps = []
        return words, deps

    def build_dependencies(self):
        for word in self.words:
            if word.governor == 0:
                # make a word for the ROOT
                governor = RootWordImpl(None)
            else:
                # id is index in words list + 1
                governor = self.words[word.governor - 1]
            self.dependencies.append((governor, word.dependency_relation, word))


class LtpParserImpl(object):
    def __init__(self, lang='zh-CN'):
        self.lang = lang

    def __call__(self, sentence:Text):
        from sagas.zh.ltp_procs import LtpProcs, ltp
        from sagas.zh.ltp_procs import extract_predicates

        # doc = spacy_doc(sents, self.lang)
        words = ltp.segmentor.segment(sentence)
        postags = ltp.postagger.postag(words)
        arcs = ltp.parser.parse(words, postags)
        roles = ltp.labeller.label(words, postags, arcs)
        netags = ltp.recognizer.recognize(words, postags)

        doc = []
        for i in range(len(words)):
            a = words[int(arcs[i].head) - 1]
            print("%s --> %s|%s|%s|%s" % (a, words[i], \
                                          arcs[i].relation, postags[i], netags[i]))
            unit = WordUnit(i=i, text=words[i],
                            dependency_relation=arcs[i].relation.lower(),
                            governor=arcs[i].head,
                            head_text=a, pos=postags[i], netag=netags[i])
            # rel = unit.dependency_relation
            doc.append(unit)

        predicts, predict_tuples=extract_predicates(words, roles, postags, arcs)
        # return LtpSentImpl(doc, predicts=predicts)
        return LtpSentImpl(doc, text=sentence, predicts=predict_tuples)

