from typing import Text, Any, Dict, List, Union, Optional
from sagas.nlu.uni_intf import RootWordImpl, WordIntf, SentenceIntf
from sagas.nlu.analspa import analspa, native_spa


class SpacyWordImpl(WordIntf):
    def setup(self, token):
        if token.dep_.upper() == 'ROOT':
            governor = 0
        else:
            governor = token.head.i + 1
        idx = token.i + 1  # start from 1
        features = {'index': idx, 'text': token.text, 'lemma': token.lemma_,
                    'upos': token.pos_, 'xpos': token.tag_,
                    'feats': '', 'governor': governor,
                    'dependency_relation': token.dep_.lower(),
                    'entity': [token.ent_type_, token.ent_iob_],
                    'term': token._.term,
                    }
        return features


class SpacySentImpl(SentenceIntf):
    def setup(self, sent):
        words = []
        for word in sent:
            words.append(SpacyWordImpl(word))
        deps = []
        return words, deps


class SpacyParserImpl(object):
    """
    >>> from sagas.nlu.uni_impl_spacy import SpacyParserImpl
    >>> from sagas.nlu.uni_viz import EnhancedViz
    >>> doc=SpacyParserImpl('ru')("Сегодня неплохая погода.")
    >>> cv = EnhancedViz(shape='egg', size='8,5', fontsize=20)
    >>> cv.analyse_doc(doc, None)
    """
    def __init__(self, lang):
        self.lang = lang

    def __call__(self, sents:Text):
        # from sagas.nlu.spacy_helper import spacy_doc
        # doc = spacy_doc(sents, self.lang)
        spa = native_spa(self.lang)
        doc, terms = spa.parse(sents)
        return SpacySentImpl(doc, text=sents)

class AnalSpaImpl(object):
    def __init__(self, lang):
        self.lang = lang

    def __call__(self, sents:Text):
        spa = analspa(self.lang)
        doc, terms=spa.parse(sents)
        return SpacySentImpl(doc, text=sents)

