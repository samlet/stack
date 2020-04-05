from typing import Text, Any, Dict, List, Union, Optional, Tuple

from sagas.nlu.ruleset_procs import cached_chunks
from anytree.node.nodemixin import NodeMixin
from anytree.node.util import _repr
from sagas.nlu.uni_intf import SentenceIntf, WordIntf, RootWordImpl
from sagas.nlu.features import feats_map
from anytree import Node, RenderTree, AsciiStyle, Walker, Resolver
from anytree.search import findall, findall_by_attr

from cachetools import cached
from cached_property import cached_property
from sagas.zh.hownet_helper import SenseTree, get_trees


class Token(object):
    def __init__(self, tok:Optional[WordIntf]):
        self.tok=tok  # readonly
        self.name=tok.dependency_relation if tok is not None else '_'

upos_mappings={'ADJ':'a', 'ADV':'r', 'NOUN':'n', 'VERB':'v'}
class AnalNode(NodeMixin, Token):
    lang: Text
    with_trans_opt: bool=False

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

    @cached_property
    def personal_pronoun_repr(self):
        def feat_or(name):
            return self.feats[name] if name in self.feats else '_'
        if 'Person' in self.feats:
            personal = feat_or('Tense') + '_' + feat_or('Person') \
                       + '_' + feat_or('Number')
            return personal
        return ''

    @property
    def verbs(self) -> Tuple['AnalNode', ...]:
        words = findall_by_attr(self, name='upos', value='VERB')
        return words

    @property
    def nouns(self) -> Tuple['AnalNode', ...]:
        words = findall_by_attr(self, name='upos', value='NOUN')
        return words

    @property
    def adjectives(self) -> Tuple['AnalNode', ...]:
        words = findall_by_attr(self, name='upos', value='ADJ')
        return words

    def rels(self, *args) -> Tuple['AnalNode', ...]:
        return findall(self, filter_=lambda n: n.dependency_relation in args)

    def resolve_rel(self, path) -> 'AnalNode':
        """
        >>> f.resolve_rel("./obl/amod")
        :param path:
        :return:
        """
        r = Resolver('dependency_relation')
        return r.get(self, path)

    def resolve_rels(self, patt) -> List['AnalNode']:
        """
        >>> f.resolve_rels("*/obj")
        :param patt:
        :return:
        """
        r = Resolver('dependency_relation')
        return r.glob(self, patt)

    def walk_to(self, node, verbose=False) -> Tuple[Any, Any, Any]:
        """Returns:
            (upwards, common, downwards): `upwards` is a list of nodes to go upward to.
            `common` top node. `downwards` is a list of nodes to go downward to.
        """
        w = Walker()
        rs= w.walk(self, node)
        if verbose:
            node_repr = lambda n: f"{n.text}({n.dependency_relation})"
            val_repr = lambda node: [node_repr(n) for n in node] if isinstance(node, tuple) else [node_repr(node)]
            print(' ._ '.join([','.join(val_repr(r)) for r in rs]))
        return rs

    def find(self, fn) -> Tuple:
        """
        >>> f.find(fn=lambda node: node.dependency_relation in ("obj"))
        :param fn:
        :return:
        """
        return findall(self, filter_=fn)

    def draw(self):
        print(RenderTree(self, style=AsciiStyle()).by_attr(
            lambda n: f"{n.dependency_relation}: {n.text} ({n.lemma}, {n.upos.lower()})"))

    @property
    def pos_abbr(self):
        att=self.tok.upos
        return upos_mappings[att] if att in upos_mappings else '*'

    def with_trans(self, val=True):
        self.with_trans_opt = val
        return self

    def is_cat(self, cat, pos='~') -> bool:
        """
        >>> f.verbs[0].is_cat('learn')
        :param cat:
        :param pos: a, r, n, v, ~(determine by upos), *
        :param with_trans:
        :return:
        """
        from sagas.nlu.utils import predicate
        if self.with_trans_opt and self.lang!='en':
            w, lang=self.axis, 'en'
        else:
            w, lang=f"{self.tok.text}/{self.tok.lemma}", self.lang
        pos=self.get_pos(pos)
        return predicate(cat, w, lang, pos)

    def get_pos(self, pos='~'):
        return self.pos_abbr if pos == '~' else pos

    @cached_property
    def axis(self):
        from sagas.nlu.translator import trans_axis
        t=self.tok
        word=t.text if t.upos.lower() in ['adj'] else t.lemma
        return trans_axis(word, self.lang, self.tok.upos)

    def is_interr(self, interr:Text) -> bool:
        from sagas.nlu.inspectors_dataset import get_interrogative
        return get_interrogative(self.tok.lemma, self.lang) == interr

    def has_role(self, **roles):
        """
        >>> f.has_role(agent='study|学习')
        :param roles:
        :return:
        """
        return any([st.has_role(**roles) for st in self.sense])

    def inherts(self, base):
        """
        >>> f.inherts('human|人')
        >>> f.nouns[0].with_trans().inherts('language|语言')
        :param base:
        :return:
        """
        return any([st.cat_of(base) for st in self.sense])

    @property
    def sense(self) -> List[SenseTree]:
        """
        >>> f.with_trans().sense
        :return:
        """
        return get_trees(self.tok.lemma if not self.with_trans_opt else self.axis)

    @property
    def word(self):
        return f"{self.tok.text}/{self.tok.lemma}"

    def synsets(self, pos='~'):
        from sagas.nlu.nlu_cli import retrieve_word_info
        rs = retrieve_word_info('get_synsets',
                                self.word, self.lang,
                                self.get_pos(pos))
        return rs

    def spec(self, pos='~'):
        from sagas.nlu.utils import get_possible_mean
        return get_possible_mean(self.synsets(pos))

    def chains(self, pos='~'):
        from sagas.nlu.nlu_cli import get_chains
        return get_chains(self.word, self.lang, self.get_pos(pos))


# @cached(cache={}) ->  因为tree-nodes是可以修改的有状态的, 所以不用cached,
#                       但anal-node.tok引用的是只读的文档结点.
def build_anal_tree(sents:Text, lang:Text, engine:Text,
                    nodecls=AnalNode):
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
    node_map = {word.index: nodecls(word, lang=lang) for word in words}
    node_map[0] = nodecls(None, sents=sents, lang=lang, engine=engine)
    tree_root = next(w for w in node_map.values() if w.governor == 0)

    def set_parent(w):
        if w.tok:
            w.parent = node_map[w.tok.governor]

    list(map(set_parent, node_map.values()))
    return tree_root

def generic_paths(f:AnalNode):
    from itertools import chain
    subjs=f.resolve_rels('*subj')
    start=subjs[0] if subjs else f
    for n in chain(f.nouns, f.adjectives):
        start.walk_to(n, verbose=True)

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
        print(RenderTree(tree_root, style=AsciiStyle()).by_attr(lambda n: f"{n.dependency_relation}: {n.text} ({n.upos.lower()})"))

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

    def paths(self, sents, lang='en', engine='stanza'):
        """
        $ python -m sagas.nlu.anal paths 'Nosotros estamos en la escuela.' es stanza
        :param sents:
        :param lang:
        :param engine:
        :return:
        """
        tree_root = build_anal_tree(sents, lang, engine)
        generic_paths(tree_root)

if __name__ == '__main__':
    import fire
    fire.Fire(AnalProcs)
