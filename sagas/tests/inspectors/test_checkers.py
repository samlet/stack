"""
$ pytest -s -v test_checkers.py
"""
from sagas.nlu.inspectors_dataset import is_negative

def test_neg():
    assert is_negative('tak bisa', 'id')
    assert not is_negative('tak', 'id')
