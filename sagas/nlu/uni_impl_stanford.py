from typing import Text, Any, Dict, List
from sagas.nlu.uni_intf import RootWordImpl, WordIntf, SentenceIntf

upos_maps={'JJ':'ADJ', 'RP':'ADP', 'RB':'ADV',
           'MD':'AUX', 'CC':'CCONJ', 'DT':'DET',
           'UH':'INTJ', 'NN':'NOUN', 'CD':'NUM',
           'POS':'PART', 'PRP':'PRON', 'NNP':'PROPN',
           'PUNC':'PUNCT', 'SYM':'SYM',
           'VB':'VERB', 'FW':'X'
          }
upos_rev_maps={'ADV':['RB', 'RBR', 'RBS', 'WRB'],
               'ADJ':['JJ', 'JJR', 'JJS'],
               'DET':['DT', 'PDT', 'WDT'],
               'SYM':['NFP', 'SYM'],
               'VERB': ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'],
               'NOUN':['NN', 'NNS', 'DTNN'],
               'PROPN':['NNP', 'NNPS'],
               'PRON':['PRP', 'PRP$', 'WP', 'WP$', 'EX'],
               'ADP':['RP', 'IN'],
               'PART':['POS', 'TO'],
              }

def get_pos_mapping(pos, default_val='X'):
    if pos in upos_maps:
        return upos_maps[pos]
    else:
        for k, v in upos_rev_maps.items():
            if pos in v:
                return k
    return default_val

def extract_words(sents, lang):
    from sagas.nlu.stanford_helper import get_sf_service
    serv=get_sf_service(lang)
    ann=serv.parse(sents, lang)
    tokens = ann['sentences'][0]['tokens']
    deps=ann['sentences'][0]['enhancedPlusPlusDependencies']
    words=[]
    for tok in tokens:
        idx=tok['index']
        dep=[d for d in deps if d['dependent']==idx][0]
        # print(dep)
        features = {'index': int(idx), 'text': tok['word'], 'lemma': tok['lemma'],
                    'upos': get_pos_mapping(tok['pos']), 'xpos': tok['pos'],
                    'feats': [], 'governor': int(dep['governor']),
                    'dependency_relation': dep['dep'].lower(),
                    'entity': [tok['ner']]
                    }
        words.append(features)
    return words

class SfWordImpl(WordIntf):
    def __init__(self, data):
        super().__init__(data)

    def setup(self, token):
        return token

class SfSentImpl(SentenceIntf):
    def setup(self, sent):
        words = []
        for word in sent:
            words.append(SfWordImpl(word))
        deps = []
        return words, deps

class SfParserImpl(object):
    """
    >>> from sagas.nlu.uni_viz_checker import *
    >>> from sagas.nlu.uni_impl_stanford import SfParserImpl
    >>> viz_check(SfParserImpl, 'en', 'Joe Smith lives in California.')
    >>> viz_check(SfParserImpl, 'en', 'Bill saw that man yesterday.')
    >>> viz_check(SfParserImpl, 'ar', "جارَك عُمَر مُتَرْجِم يا رَواد.")
    >>> viz_check(SfParserImpl, 'ar', '‫هو هنا وهي أيضاً.‬')
    """
    def __init__(self, lang):
        self.lang = lang

    def __call__(self, sents:Text):
        doc = extract_words(sents, self.lang)
        return SfSentImpl(doc, text=sents)

