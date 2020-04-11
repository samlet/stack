"""
$ pytest -s -v test_anal_zh.py
"""
def test_zh():
    from sagas.nlu.anal import build_anal_tree, Doc, AnalNode
    f = build_anal_tree('附近有什么好吃的饭馆', 'zh', 'ltp')
    f.draw()
    assert (f/'obj').deprel=='obj'
    assert ['饭馆', '饭馆'] == [f.resolve_rel("obj").text,
        f.resolve_rels("obj*")[0].text]


