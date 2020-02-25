from typing import Text, Any, Dict, List
from nltk.corpus import wordnet as wn
from sagas.nlu.omw_extended import langsets, omw_ext
from sagas.nlu.locales import is_available

hypo = lambda s: s.hyponyms()
hyper = lambda s: s.hypernyms()
# omw = OmwExtended()

def get_word_lemmas(synset, lang) -> List[Text]:
    if not is_available(lang):
        les = [w['word'] for w in omw_ext.get_word(lang, synset.offset(), synset.pos())]
    else:
        les = synset.lemma_names(langsets[lang])
    return list(filter(lambda w: w is not None,les))

def get_lemmas(synsets, target_langs) -> List[Any]:
    rs=[]
    for idx, c in enumerate(synsets):
        # print('%d.'%idx, c.name())
        chain={'index':idx, 'name':c.name(), 'hyper':[]}
        for c_c in [c]+list(c.closure(hyper)):
            level={'name':c_c.name(), 'definition':c_c.definition(), 'records':[]}
            for lang in target_langs:
                # les=c_c.lemma_names(langsets[lang])
                # if not is_available(lang):
                #     les = [w['word'] for w in omw_ext.get_word(lang, c_c.offset(), c_c.pos())]
                # else:
                #     les = c_c.lemma_names(langsets[lang])
                les=get_word_lemmas(c_c, lang)
                if len(les)>0:
                    level['records'].append({'lang':lang, 'lemmas':les})
            chain['hyper'].append(level)
        rs.append(chain)
    return rs

def explore(word, lang='en', target_langs=None) -> List[Any]:
    if target_langs is None:
        target_langs = ['en', 'fr', 'ja', 'zh']
    sets = wn.synsets(word, pos=None, lang=langsets[lang])
    rs = get_lemmas(sets, target_langs)
    return rs

