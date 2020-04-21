from typing import Text, Any, Dict, List, Union, Optional, Tuple

from sagas.nlu.anal_conf import AnalConf


class AnalSpa(object):
    """
    >>> from sagas.nlu.analspa import analspa
    >>> spa=analspa('ja')
    >>> spa.add_pats("TerminologyList", ["主FAX番号"])
    >>> doc,terms=spa.parse('主FAX番号はありますか')
    >>> print([(w.lemma_, w._.term) for w in doc])
    >>> spa.vis(doc)
    """
    def __init__(self, lang):
        from spacy.matcher import PhraseMatcher
        from sagas.nlu.stanza_helper import get_nlp
        from spacy_stanza import StanzaLanguage

        self.lang=lang
        snlp = get_nlp(lang)
        self.nlp = StanzaLanguage(snlp)
        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        self.conf=AnalConf(lang)
        self.conf.setup(self)

    def add_pats(self, pat_name, pat_text_ls:List[Text]):
        patterns=[self.nlp.make_doc(text) for text in pat_text_ls]
        self.matcher.add(pat_name, None, *patterns)

    def parse(self, sents:Text) -> Tuple[Any, List[Dict]]:
        doc = self.nlp(sents)
        matches = self.matcher(doc)
        spans = []
        terms=[]
        for match_id, start, end in matches:
            span = doc[start:end]
            match_id_string = self.nlp.vocab.strings[match_id]
            term={'term':match_id_string, 'value': span.text}
            terms.append(term)
            spans.append((span, term))

        with doc.retokenize() as retokenizer:
            for span, term in spans:
                retokenizer.merge(span, attrs={"_": {"term": term}})

        return doc, terms

    def vis(self, doc):
        from spacy import displacy
        displacy.render([doc], style="dep")

spa_modules={}
def analspa(lang) -> AnalSpa:
    if lang not in spa_modules:
        spa_modules[lang]=AnalSpa(lang)
    return spa_modules[lang]

def init_analspa():
    from spacy.tokens import Token
    Token.set_extension("term", default={})

init_analspa()
