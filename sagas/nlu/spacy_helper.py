from spacy.symbols import nsubj, VERB
import pandas as pd

lang_spacy_mappings={'en':['en_core_web_sm', 'en_core_web_md'],
                     'fr':['fr_core_news_sm', 'fr_core_news_md'],
                     'el':['el-core-news-sm', 'el-core-news-md'],
                     'de':['de-core-news-sm', 'de-core-news-md'],
                     'pt':['pt-core-news-sm', 'pt-core-news-sm'],
                     'nl':['nl-core-news-sm', 'nl-core-news-sm'],
                     'it':['it-core-news-sm', 'it-core-news-sm'],
                     'es':['es-core-news-sm', 'es-core-news-sm'],
                     'no':['nb_core_news_sm', 'nb_core_news_sm'], # Norwegian Bokmaal
                     'lt':['lt_core_news_sm', 'lt_core_news_sm'], # Lithuanian(立陶宛语)
                     'ru':['/pi/ru2', '/pi/ru2'],
                     }

def is_available(lang):
    return lang in lang_spacy_mappings

class SpacyManager(object):
    def __init__(self):
        self.models={}

    def get_model(self, lang='en', simple=True):
        import spacy

        idx=0 if simple else 1
        spacy_model = lang_spacy_mappings[lang][idx]
        spacy_model=spacy_model.replace('-','_')
        if spacy_model not in self.models:
            spacy_nlp = spacy.load(spacy_model)
            self.models[spacy_model]=spacy_nlp
        else:
            spacy_nlp=self.models[spacy_model]
        return spacy_nlp

spacy_mgr=SpacyManager()

def spacy_doc(sents, lang):
    spacy_nlp = spacy_mgr.get_model(lang)
    return spacy_nlp(sents)

def get_verbs(doc):
    verbs = set()
    for possible_subject in doc:
        if possible_subject.dep == nsubj and possible_subject.head.pos == VERB:
            verbs.add(possible_subject.head)
    return verbs

def get_verb_lemmas(doc):
    verbs = []
    for possible_subject in doc:
        if possible_subject.dep == nsubj and possible_subject.head.pos == VERB:
            verbs.append(possible_subject.head.lemma_)
    return verbs

def get_inflects(word):
    from pyinflect import getAllInflections, getInflection
    return getAllInflections('watch')

def chunks_df(doc):
    toks = {'text': [], 'root_text': [], 'root_dep': [], 'head': []}
    for chunk in doc.noun_chunks:
        # print(chunk.text, chunk.root.text, chunk.root.dep_,
        #      chunk.root.head.text)
        toks['text'].append(chunk.text)
        toks['root_text'].append(chunk.root.text)
        toks['root_dep'].append(chunk.root.dep_)
        toks['head'].append(chunk.root.head.text)
    df = pd.DataFrame(toks)
    return df

def doc_df(doc):
    toks={'text':[], 'lemma':[], 'pos':[], 'tag':[], 'dep':[]}
    for token in doc:
        # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
        #        token.shape_, token.is_alpha, token.is_stop)
        toks['text'].append(token.text)
        toks['lemma'].append(token.lemma_)
        toks['pos'].append(token.pos_)
        toks['tag'].append(token.tag_)
        toks['dep'].append(token.dep_)

    df = pd.DataFrame(toks)
    return df

def nav_tree(doc):
    for token in doc:
        print(token.text, token.dep_, token.head.text, token.head.pos_,
              [child for child in token.children])


def doc_collect(doc):
    toks={'text':[], 'lemma':[], 'pos':[], 'tag':[], 'dep':[]}
    for token in doc:
        # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
        #        token.shape_, token.is_alpha, token.is_stop)
        toks['text'].append(token.text)
        toks['lemma'].append(token.lemma_)
        toks['pos'].append(token.pos_)
        toks['tag'].append(token.tag_)
        toks['dep'].append(token.dep_)
    return toks

def get_lemmas(doc):
    toks = doc_collect(doc)
    lemmas = ' '.join(toks['lemma'])
    return lemmas
