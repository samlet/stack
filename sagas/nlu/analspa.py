from typing import Text, Any, Dict, List, Union, Optional, Tuple

class AnalSpa(object):
    """
    >>> from sagas.nlu.analspa import AnalSpa
    >>> spa=AnalSpa('ja')
    >>> spa.add_pats("TerminologyList", ["主FAX番号"])
    >>> doc,terms=spa.parse('主FAX番号はありますか')
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
            terms.append({'term':match_id_string, 'value': span.text})
            spans.append(span)

        with doc.retokenize() as retokenizer:
            for span in spans:
                retokenizer.merge(span)

        return doc, terms

    def vis(self, doc):
        from spacy import displacy
        displacy.render([doc], style="dep")

