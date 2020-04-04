from typing import Text, Any, Dict, List, Union, Optional

from sagas.nlu.ruleset_procs import cached_chunks
from anytree.node.nodemixin import NodeMixin
from anytree.node.util import _repr
from sagas.nlu.uni_intf import SentenceIntf, WordIntf, RootWordImpl
from sagas.nlu.features import feats_map
from anytree import Node, RenderTree, AsciiStyle, Walker, Resolver
from anytree.search import findall, findall_by_attr

from cachetools import cached

class Token(object):
    def __init__(self, tok:Optional[WordIntf]):
        self.tok=tok
        self.name=tok.dependency_relation if tok is not None else '_'

class AnalNode(NodeMixin, Token):
    def __init__(self, tok:Optional[WordIntf], parent=None, children=None, **kwargs):
        super(AnalNode, self).__init__(tok)
        self.__dict__.update(kwargs)
        if tok:
            self.__dict__.update(tok.ctx)
            self.feats=feats_map(tok.feats)
        self.parent = parent
        if children:
            self.children = children

    def __repr__(self):
        return _repr(self)

@cached(cache={})
def build_anal_tree(sents:Text, lang:Text, engine:Text):
    """
    >>> from sagas.nlu.anal import build_anal_tree
    >>> from anytree.search import findall, findall_by_attr
    >>> f=build_anal_tree(sents, lang, engine)
    >>> words = findall_by_attr(f, name='upos', value='VERB')
    >>> objs = findall(words[0], filter_=lambda n: n.dependency_relation in ("obj"))

    :param sents:
    :param lang:
    :param engine:
    :return:
    """
    chunks = cached_chunks(sents,
                           source=lang,
                           engine=engine)
    words = chunks['doc'].words
    node_map = {word.index: AnalNode(word) for word in words}
    node_map[0] = AnalNode(None)
    tree_root = next(w for w in node_map.values() if w.governor == 0)

    def set_parent(w):
        if w.tok:
            w.parent = node_map[w.tok.governor]

    list(map(set_parent, node_map.values()))
    return tree_root

class AnalProcs(object):
    def doc(self, sents, lang='en', engine='stanza'):
        """
        $ python -m sagas.nlu.anal doc 'Nosotros estamos en la escuela.' es stanza
        $ python -m sagas.nlu.anal doc '우리는 사람들을 이해하고 싶어요.' ko

        :param sents:
        :param lang:
        :param engine:
        :return:
        """
        chunks = cached_chunks(sents,
                               source=lang,
                               engine=engine)
        return chunks['doc'].as_json

    def tree(self, sents, lang='en', engine='stanza'):
        """
        $ python -m sagas.nlu.anal tree 'Nosotros estamos en la escuela.' es stanza
        :param sents:
        :param lang:
        :param engine:
        :return:
        """
        tree_root=build_anal_tree(sents, lang, engine)
        print(RenderTree(tree_root, style=AsciiStyle()).by_attr(lambda n: f"{n.dependency_relation}: {n.text}"))

    def verbs(self, sents, lang='en', engine='stanza'):
        """
        $ python -m sagas.nlu.anal verbs 'Nosotros estamos en la escuela.' es stanza
        :param sents:
        :param lang:
        :param engine:
        :return:
        """
        tree_root = build_anal_tree(sents, lang, engine)
        words = findall_by_attr(tree_root, name='upos', value='VERB')
        return words

if __name__ == '__main__':
    import fire
    fire.Fire(AnalProcs)
