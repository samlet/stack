"""
$ pytest -s -v test_senses.py
"""
from sagas.zh.hownet_helper import build_trees, get_word_sense, get_trees
import logging
import pytest

@pytest.mark.parametrize(
    "word, cat, roles",
    [
        ('大学生', 'human|人', dict(agent='study|学习')),
        ('小学生', 'human|人', dict(agent='study|学习')),
        ('校长', 'human|人', dict(agent='manage|管理', HostOf='Occupation|职位')),
    ],
)
def test_hownet(word, cat, roles):
    from sagas.tool.servant_delegator import Delegator
    from sagas.zh.hownet_helper import logger
    logger.setLevel(logging.DEBUG)

    trees = Delegator().sememes(word=word)

    sts=build_trees(trees)
    st=sts[0]
    assert st.cat_of(cat)
    assert st.has_role(**roles)

@pytest.mark.parametrize(
    "word, cat, roles",
    [
        ('大学生', 'human|人', dict(agent='study|学习')),
        ('小学生', 'human|人', dict(agent='study|学习')),
        ('校长', 'human|人', dict(agent='manage|管理', HostOf='Occupation|职位')),
    ],
)
def test_sense(word, cat, roles):
    from sagas.zh.hownet_helper import logger
    logger.setLevel(logging.DEBUG)

    sts=get_trees(word)
    print('unique trees count', len(sts))
    st=sts[0]
    assert st.cat_of(cat)
    assert st.has_role(**roles)

