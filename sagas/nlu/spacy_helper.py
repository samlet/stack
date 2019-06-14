from spacy.tokens import Doc
import spacy
from spacy.symbols import nsubj, VERB
import pandas as pd

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
