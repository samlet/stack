from typing import Text, Any, Dict, List, Union
from sagas.nlu.uni_intf import WordIntf, SentenceIntf

class StanzaWordImpl(WordIntf):
    from stanza.models.common.doc import Word
    def setup(self, data:Word):
        features_map = {'text':'text',
                        'lemma': 'lemma',
                        'upos':'upos', 'xpos':'xpos',
                        'feats': 'feats',
                        'dependency_relation':'deprel'
                        }
        int_map={'index':'id', 'governor':'head'}
        indexes={k: int(getattr(data, v)) for k,v in int_map.items() if getattr(data, v) is not None}
        attrs = {k: getattr(data, v) for k,v in features_map.items() if getattr(data, v) is not None}
        attrs['entity']=[data.parent.ner] if data.parent and data.parent.ner else []

        return {**indexes, **attrs}


class StanzaSentImpl(SentenceIntf):
    from stanza.models.common.doc import Sentence
    def setup(self, sent:Sentence):
        words = []
        for word in sent.words:
            words.append(StanzaWordImpl(word))
        deps = []
        for dep in sent.dependencies:
            # (governor, word.dependency_relation, word)
            deps.append((StanzaWordImpl(dep[0]), dep[1], StanzaWordImpl(dep[2])))
        return words, deps


class StanzaParserImpl(object):
    def __init__(self, lang):
        self.lang = lang

    def __call__(self, sents:Text):
        from sagas.nlu.stanza_helper import get_nlp
        from sagas.nlu.transliterations import translits

        preprocs={'sr':lambda : translits.translit(sents, self.lang),
                  }
        nlp = get_nlp(self.lang)
        if self.lang in preprocs:
            sents=preprocs[self.lang]()
        doc = nlp(sents)
        return StanzaSentImpl(doc.sentences[0], text=sents)

