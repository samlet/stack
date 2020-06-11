from typing import Text, Any, Dict, List, Union, Optional, Tuple

from sagas.nlu.anal_conf import anal_conf
from spacy.tokens import DocBin

pretokenized_langs = ['zh']
def get_model(lang, provider, enable_pretoken=False):
    def stanza_model():
        from sagas.nlu.stanza_helper import get_nlp
        from spacy_stanza import StanzaLanguage
        if enable_pretoken:
            snlp = get_nlp(lang) if lang not in pretokenized_langs else get_nlp(lang, pretokenized=True)
        else:
            snlp = get_nlp(lang)
        return StanzaLanguage(snlp)

    def spacy_model():
        from sagas.nlu.spacy_helper import spacy_mgr
        return spacy_mgr.get_model(lang)

    return stanza_model() if provider == 'stanza' else spacy_model()

class AnalSpa(object):
    """
    >>> from sagas.nlu.analspa import analspa
    >>> spa=analspa('ja')
    >>> spa.add_pats("TerminologyList", ["主FAX番号"])
    >>> doc,terms=spa.parse('主FAX番号はありますか')
    >>> print([(w.lemma_, w._.term) for w in doc])
    >>> spa.vis(doc)
    """
    def __init__(self, lang, provider='stanza', enable_pretoken=False):
        from spacy.matcher import PhraseMatcher

        self.lang=lang
        self.provider=provider
        self.enable_pretoken=enable_pretoken
        self.nlp = get_model(lang, self.provider, enable_pretoken)
        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        self.conf=anal_conf(lang)
        self.conf.setup(self)

    def add_pats(self, pat_name, pat_text_ls:List[Text]):
        patterns=[self.nlp.make_doc(text) for text in pat_text_ls]
        self.matcher.add(pat_name, None, *patterns)

    def _parse_pretokenized(self, sents):
        import jieba
        seg_list = jieba.cut(sents)
        toks=' '.join(seg_list)
        doc = self.nlp(toks)
        return doc

    def parse(self, sents:Text, merge=True) -> Tuple[Any, List[Dict]]:
        if self.enable_pretoken:
            doc = self.nlp(sents) if self.lang not in pretokenized_langs else self._parse_pretokenized(sents)
        else:
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

        if merge:
            doc=self._merge_doc(doc)
        return doc, terms

    @staticmethod
    def _merge_doc(doc):
        from spacy.util import filter_spans
        spans = list(doc.ents) + list(doc.noun_chunks)
        spans = filter_spans(spans)
        with doc.retokenize() as retokenizer:
            for span in spans:
                retokenizer.merge(span)
        return doc

    @staticmethod
    def vis(doc):
        from spacy import displacy
        displacy.render([doc], style="dep")

    def graph(self, sents, merge=True):
        from sagas.tracker_jupyter import enable_jupyter_tracker
        from sagas.nlu.uni_impl_spacy import SpacySentImpl
        from sagas.nlu.uni_viz import vis_doc
        enable_jupyter_tracker()
        doc, terms = self.parse(sents, merge=merge)
        return vis_doc(doc, sents, SpacySentImpl)

_spa_bridge_modules={}
def analspa(lang) -> AnalSpa:
    if lang not in _spa_bridge_modules:
        _spa_bridge_modules[lang]=AnalSpa(lang)
    return _spa_bridge_modules[lang]

_spa_modules={}
def native_spa(lang) -> AnalSpa:
    if lang not in _spa_modules:
        _spa_modules[lang]=AnalSpa(lang, provider='spacy')
    return _spa_modules[lang]

def init_analspa():
    from spacy.tokens import Token
    Token.set_extension("term", default={})

init_analspa()

def write_doc_to(proto, file):
    from os.path import expanduser
    with open(expanduser(file), "wb") as f:
        f.write(proto)

def read_doc(lang, file) -> List[Any]:
    from os.path import expanduser
    nlp = get_model(lang, provider='spacy')
    with open(expanduser(file), "rb") as f:
        doc_bin = DocBin().from_bytes(f.read())
        docs = list(doc_bin.get_docs(nlp.vocab))
        return docs

def write_docs(texts, attrs, lang, file, provider='spacy'):
    from tqdm import tqdm
    nlp = get_model(lang, provider=provider)
    doc_bin = DocBin(attrs=[a.upper() for a in attrs], store_user_data=True)
    # doc_bin = DocBin(attrs=["DEP", "HEAD"])
    # for doc in nlp.pipe(texts):
    # the tqdm library just wraps a loop. When you call it around nlp.pipe,
    # the loop you're wrapping are the individual batches.
    for doc in tqdm(nlp.pipe(texts)):
        doc_bin.add(doc)
    bytes_data = doc_bin.to_bytes()
    write_doc_to(bytes_data, file)

