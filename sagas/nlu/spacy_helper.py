from spacy.tokens import Doc
import spacy
from spacy.symbols import nsubj, VERB

def get_verbs(doc):
    verbs = set()
    for possible_subject in doc:
        if possible_subject.dep == nsubj and possible_subject.head.pos == VERB:
            verbs.add(possible_subject.head)
    return verbs

def get_inflects(word):
    from pyinflect import getAllInflections, getInflection
    return getAllInflections('watch')

