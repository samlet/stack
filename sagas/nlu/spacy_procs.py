from __future__ import unicode_literals, print_function, division
from io import open
import unicodedata
import string
import re
import random
import spacy
from spacy.symbols import nsubj, POS, NOUN, VERB, ADJ, PUNCT

def print_nouns(doc):
    for chunk in doc.noun_chunks:
        print(chunk.text, "☼" + chunk.root.text, chunk.root.dep_,
              "☈" + chunk.root.head.text)

# cell 2
def get_root(doc, merge=False):
    root = [token for token in doc if token.head == token][0]
    subject = None
    # print("root:", root.text)
    lefts = list(root.lefts)
    if len(lefts) > 0:
        subject = lefts[0]
        subject_index = subject.i
        if merge:
            span = doc[doc[subject_index].left_edge.i: doc[subject_index].right_edge.i + 1]
            subject = span.merge()
            # regeting the root node
            root = [token for token in doc if token.head == token][0]
    return root, subject


def print_tokens(doc, root):
    for token in doc:
        # token.head.pos_
        mark = str(token.i)
        if token == root:
            mark = "⊙"
        elif token.head.i == root.i:
            mark = "☑"
        if token.pos not in [PUNCT]:
            print("\t", mark, token.text, token.dep_, "☈" + token.head.text,
                  [child for child in token.children])


def print_verbs(doc):
    # Finding a verb with a subject from below — good
    verbs = set()
    for possible_subject in doc:
        if possible_subject.dep == nsubj and possible_subject.head.pos == VERB:
            verbs.add(possible_subject.head)
    print("verbs+:", verbs)


def print_call_format(token):
    result = []
    for child in token.children:
        if not child.is_punct:
            result.append("{}:{}".format(child.dep_, normalizeString(child.lemma_)))
    print("{}({})".format(normalizeString(token.lemma_), ", ".join(result)))


# cell 3
def analyse(doc):
    root, subject = get_root(doc, False)
    print("root:", root.text, spacy.explain(root.pos_))
    if subject:
        print("subject:", subject.text, subject.i)
    print_verbs(doc)
    print_call_format(root)
    print("------------")
    print_tokens(doc, root)
    print("------------ noun_chunks")
    print_nouns(doc)
    print("------------ merge subject")
    root, subject = get_root(doc, True)
    print("root:", root.text)
    if subject:
        print("subject:", subject.text, subject.i)
    print("------------")
    print_tokens(doc, root)

# Turn a Unicode string to plain ASCII, thanks to
# http://stackoverflow.com/a/518232/2809427
def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

# Lowercase, trim, and remove non-letter characters
def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?-]+", r" ", s)
    return s

class SpacyProcs(object):
    # def __init__(self):
    #     self.nlp = spacy.load('en_core_web_sm')

    def spacy_doc(self, sents, lang):
        from sagas.nlu.spacy_helper import spacy_mgr
        spacy_nlp = spacy_mgr.get_model(lang)
        return spacy_nlp(sents)

    def stuffs(self):
        """
        $ python -m sagas.nlu.spacy_procs stuffs
        :return:
        """
        # nlp = spacy.load('en_core_web_md')
        doc = self.spacy_doc(u"Credit and mortgage account holders must submit their requests", 'en')
        analyse(doc)
        ## main
        doc = self.spacy_doc(u"You give this cheese to your child", 'en')
        analyse(doc)  ## main
        print("ok.")

    def ents(self, sents, lang='en'):
        """
        $ python -m sagas.nlu.spacy_procs ents 'New York'
        $ python -m sagas.nlu.spacy_procs ents 'I am from China'
        :param sents:
        :param lang:
        :return:
        """
        import sagas
        rs = []
        doc=self.spacy_doc(sents, lang)
        for ent in doc.ents:
            rs.append((ent.text, ent.start_char, ent.end_char, ent.label_))
        r= sagas.to_df(rs, ['word', 'start', 'end', 'entity'])
        sagas.print_df(r)

if __name__ == '__main__':
    import fire
    fire.Fire(SpacyProcs)



