"""
$ pytest -s -v test_anal_ja.py
"""
def test_ja():
    from sagas.nlu.anal import build_anal_tree, Doc, AnalNode
    f = build_anal_tree('コーヒーを ミルク付きで お願い します 。', 'ja', 'knp')
    f.draw()
    assert ['珈琲', '珈琲'] == [f.resolve_rel("obj").lemma,
                            f.resolve_rels("obj*")[0].lemma]


