"""
$ pytest -s -v test_anal.py
"""

def test_as_desc():
    from sagas.nlu.anal import build_anal_tree, Doc, AnalNode
    f = build_anal_tree('Nuestro horario es de nueve a cinco.', 'es', 'stanza')
    desc = f.as_desc()
    assert (desc.subj.text, desc.subj_spec, desc.aux.lemma, desc.desc.as_num()) \
           == ('horario', 'schedule', 'ser', 9)

