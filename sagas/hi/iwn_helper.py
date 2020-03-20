from typing import Text, Any, Dict, List, Union

from sagas.nlu.utils import norm_pos
from sagas.tool.servant_delegator import Delegator

def inherit_axis(word: Text, pos: Text, axis:Text):
    """
    >>> inherit_axis(axis), inherit_axis('seba|apple'), inherit_axis('vanaspati|tree'),
    >>> inherit_axis('vanaspati|err')

    :param word:
    :param pos:
    :param axis:
    :return:
    """
    key,anno=axis.split('|')
    pos=norm_pos(pos)
    rs = Delegator().iwn_hypers(word=word, pos=pos)
    syns=[syn for syn in rs if syn['synset']==key]
    if syns:
        for syn in syns:
            trans=syn['trans']
            if anno==trans['word'] or anno in trans['candidates']:
                return True
    return False

