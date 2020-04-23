"""
$ pytest -s -v test_warehouse.py
"""
def test_gid():
    from sagas.nlu.warehouse import Warehouse
    wh = Warehouse.create()
    gid = 'UHJvZHVjdFR5cGU6QUdHUkVHQVRFRA=='
    val = wh.resolve_entity(gid).value
    assert 'ProductType'==val.getEntityName()
    assert gid==wh.get_gid(val)

