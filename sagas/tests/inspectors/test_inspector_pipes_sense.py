"""
$ pytest -s -v test_inspector_pipes_sense.py
"""
import logging
from sagas.nlu.parse_client_helper import build_context
from sagas.nlu.pipes import sense_cond
from sagas.nlu.rules_header import *
from sagas.nlu import inspectors, inspector_pipes
from pprint import pprint
import pytest

all_of = lambda *arg: all([r[1] for r in arg])

@pytest.mark.parametrize(
    "sents, lang",
    [
        ('What do you think about the war?', 'en'),
    ],
)
def test_pipes_sense(sents, lang):
    inspectors.logger.setLevel(logging.DEBUG)
    inspector_pipes.logger.setLevel(logging.DEBUG)

    data = {'lang': lang, "sents": sents}
    ctx, pat = next(build_context(data, 'verb', name='_test_'))

    rs=pat(pipes(collect=['verb', 'noun']),
           pipes(sense=sense_cond.is_cat('/obl', 'fact|事情')
                 .with_roles(domain='military|军')),
           )
    pprint((rs[1], rs[0], rs[3].results))
    assert all_of(rs)

    rs = pat(pipes(collect=['verb', 'noun']),
             pipes(sense=sense_cond.has_roles('/obl', domain='military|军')),
             )
    pprint((rs[1], rs[0], rs[3].results))
    assert all_of(rs)
