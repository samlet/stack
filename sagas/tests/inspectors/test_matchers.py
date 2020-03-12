"""
$ pytest -s -v test_matchers.py
"""
from sagas.nlu.ruleset_procs import list_words, cached_chunks, get_main_domains
from sagas.conf.conf import cf

def test_chunk_matcher():
    from sagas.nlu.uni_chunks import get_chunk
    from pampy import match, _

    # She denied being my mother
    sents = 'Ela negou ser minha mãe.'
    lang = 'pt'
    domain = 'verb_domains'
    chunks = cached_chunks(sents, lang, cf.engine(lang))

    cla = 'obl'
    raw = get_chunk(chunks, domain, cla, lambda w: {'rel': w.dependency_relation,
                                                    'pos': w.upos.lower(),
                                                    'word': f"{w.text}/{w.lemma}"})
    rs = {e['rel']: e for e in raw}
    r=match(rs, {'cop': {'word': _}, 'obl': {'pos': 'noun', 'word': _}}, lambda *arg: arg,
          _, "anything else"
          )
    assert r==('ser/ser', 'mãe/mãe')

    r=match(rs, {_: {'pos': 'aux'}, 'obl': {'pos': 'noun', 'word': _}}, lambda *arg: arg,
          _, "anything else"
          )
    assert r==('cop', 'mãe/mãe')

def test_class_matcher():
    from sagas.nlu.uni_chunks import get_chunk
    from pampy import match, _
    from dataclasses import dataclass

    @dataclass
    class WordData:
        index: int
        rel: str
        pos: str
        word: str

        # She denied being my mother
    sents = 'Ela negou ser minha mãe.'
    lang = 'pt'
    domain = 'verb_domains'
    chunks = cached_chunks(sents, lang, cf.engine(lang))

    cla = 'obl'
    ana = get_chunk(chunks, domain, cla, lambda w: WordData(index=w.index,
                                                            rel=w.dependency_relation,
                                                            pos=w.upos.lower(),
                                                            word=f"{w.text}/{w.lemma}"))
    t_rs=[]
    for word_data in ana:
        r = match(word_data,
                  WordData(_, _, 'aux', _), lambda *arg: f"aux: {arg[2]}",
                  WordData(_, 'obl', 'noun', _), lambda *arg: arg,
                  _, None
                  )
        t_rs.append(r)
    assert t_rs==['aux: ser/ser',
                  None,
                  (5, 'mãe/mãe')]
