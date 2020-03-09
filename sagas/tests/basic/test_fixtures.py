"""
$ pytest -q test_fixtures.py
"""
import pytest


@pytest.fixture()
def hello():
    return "hello"

def test_string(hello):
    assert hello == "hello", "fixture should return hello"

