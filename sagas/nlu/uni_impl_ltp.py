from typing import Text, Any, Dict, List

from sagas.nlu.analz_base import Docz
from sagas.nlu.uni_intf import RootWordImpl, WordIntf, SentenceIntf
import logging
logger = logging.getLogger(__name__)

# upos_maps={'a':'ADJ', 'p':'ADP', 'd':'ADV',
#            'u':'AUX', 'c':'CCONJ', 'h':'DET',
#            'e':'INTJ', 'n':'NOUN', 'm':'NUM',
#            'z':'PART', 'r':'PRON', 'nh':'PROPN',
#            'wp':'PUNCT', 'ws':'SYM',
#            'v':'VERB', 'x':'X'
#           }
upos_maps={'a': 'ADJ', 'b': 'NOUN', 'c': 'CCONJ', 'd': 'ADV', 'e': 'INTJ',
           'g': 'NOUN', 'h': 'PART', 'i': 'NOUN', 'j': 'PROPN', 'k': 'PART',
           'm': 'NUM', 'n': 'NOUN', 'nd': 'NOUN', 'nh': 'PROPN', 'ni': 'PROPN',
           'nl': 'NOUN', 'ns': 'PROPN', 'nt': 'NOUN', 'nz': 'PROPN', 'o': 'INTJ',
           'p': 'ADP', 'q': 'NOUN', 'r': 'PRON', 'u': 'PART', 'v': 'VERB',
           'wp': 'PUNCT', 'ws': 'X', 'x': 'SYM', 'z': 'ADV'}
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
    def __init__(self, i, text, dependency_relation,
                 governor, head_text, pos, netag, term):
        self.i=i
        self.text=text
        self.lemma=text
        self.dependency_relation=dependency_relation
        self.governor=governor
        self.head_text=head_text
        self.pos=pos
        self.upos=get_pos_mapping(pos)

        self.netag=netag
        self.term=term

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
                    'feats': '', 'governor': int(governor),
                    'dependency_relation': rel,
                    'entity': [token.netag],
                    'term': token.term,
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
                governor = RootWordImpl()
            else:
                # id is index in words list + 1
                governor = self.words[word.governor - 1]
            self.dependencies.append((governor, word.dependency_relation, word))


class LtpParserBase(object):
    def parse(self, sents:Text) -> Docz:
        pass

    def __call__(self, sents:Text):
        import opencc
        from sagas.zh.ltp_procs import extract_predicates
        sentence = opencc.convert(sents)  # convert to Simplified Chinese
        doc=self.parse(sentence)
        toks = []
        for i in range(len(doc.words)):
            a = doc.words[int(doc.arcs[i].head) - 1]
            logger.debug("%s --> %s|%s|%s|%s" % (a, doc.words[i], doc.arcs[i].relation, doc.postags[i], doc.netags[i]))

            unit = WordUnit(i=i, text=doc.words[i],
                            dependency_relation=doc.arcs[i].relation.lower(),
                            governor=doc.arcs[i].head,
                            head_text=a, pos=doc.postags[i],
                            netag=doc.netags[i],
                            term=doc.terms[i] if doc.terms else {},
                            )
            # rel = unit.dependency_relation
            toks.append(unit)

        predicts, predict_tuples=extract_predicates(doc.words, doc.roles, doc.postags, doc.arcs)
        # return LtpSentImpl(doc, predicts=predicts)
        return LtpSentImpl(toks, text=sentence, predicts=predict_tuples)

class LtpParserImpl(LtpParserBase):
    def __init__(self, lang='zh-CN'):
        self.lang = lang

    def parse(self, sents) -> Docz:
        from sagas.zh.ltp_procs import ltp

        words = ltp.segmentor.segment(sents)
        postags = ltp.postagger.postag(words)
        arcs = ltp.parser.parse(words, postags)
        roles = ltp.labeller.label(words, postags, arcs)
        netags = ltp.recognizer.recognize(words, postags)
        return Docz(words, postags, arcs, roles, netags, [])

class AnalzImpl(LtpParserBase):
    def parse(self, sents) -> Docz:
        from sagas.nlu.analz import analz
        return analz.parse(sents)

