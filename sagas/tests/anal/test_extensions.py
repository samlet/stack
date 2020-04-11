"""
$ pytest -s -v test_extensions.py
"""
def test_conf():
    from sagas.nlu.anal import build_anal_tree, Doc, AnalNode
    from sagas.nlu.anal_corpus import model_info
    f = build_anal_tree('Ördek filin üzerinde.', 'tr', 'stanza')
    # f.draw()
    assert 'AnalNode_tr'==type(f).__name__
    assert 'Doc' == type(f.doc).__name__

