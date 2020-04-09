from typing import Text, Any, Dict, List, Union, Optional, Tuple, Set
from dataclasses import dataclass

from sagas.nlu.ruleset_procs import cached_chunks
from anytree.node.nodemixin import NodeMixin
from anytree.node.util import _repr
from sagas.nlu.uni_intf import SentenceIntf, WordIntf, RootWordImpl
from sagas.nlu.features import extract_feats_map
from anytree import Node, RenderTree, AsciiStyle, Walker, Resolver
from anytree.search import findall, findall_by_attr

from cachetools import cached
from cached_property import cached_property
from sagas.zh.hownet_helper import SenseTree, get_trees

class Doc(NodeMixin, object):
    """
    Integrate with extractors
    >>> f=build_anal_tree('2008年12月に上海に行きたいです。', 'ja', 'stanza')
    >>> from sagas.nlu.inspector_extractor import ex_translit
    >>> if ex_translit('', 'たいです', '', f.doc):
    >>>     print(f.doc.resultset)
    """
    resultset: List[Dict[Text, Any]]=[]
    domain_name:str='anal'
    sents: Text
    lang: Text
    engine: Text
    index_data: Dict[Text, Any]={}
    doc: SentenceIntf

    def __init__(self, parent=None, children=None, **kwargs):
        self.__dict__.update(kwargs)
        self.parent = parent
        if children:
            self.children = children

    def __repr__(self):
        return _repr(self)

    def add_result(self, inspector: Text, provider: Text, part_name: Text,
                   val:Any, delivery_type='slot'):
        from sagas.nlu.utils import is_full_domain_path
        if not is_full_domain_path(part_name):
            part_name = self.domain_name + ':' + part_name
        self.resultset.append({'inspector': inspector,
                              'provider': provider,
                              'part': part_name,
                              'value': val,
                              'delivery': delivery_type,
                              'pattern': '_',
                              })

    def ensure_data(self, provider_name:Text):
        from sagas.nlu.anal_providers import get_provider_by_name
        if provider_name not in self.index_data:
            data = get_provider_by_name(provider_name)(self, provider_name)
            self.index_data[provider_name] = data
        else:
            data = self.index_data[provider_name]
        return data

    def get_index_data(self, provider_name:Text, index:int):
        data=self.ensure_data(provider_name)
        return data[index] if index in data else None

class Token(object):
    def __init__(self, tok:Optional[WordIntf]):
        self.tok=tok  # readonly
        self.name=tok.dependency_relation if tok is not None else '_'

def node_or(nodels):
    return nodels[0] if nodels else None
def node_desc(n:'AnalNode'):
    return f"{n.tok.lemma}({n.deprel})" if n else '_'

@dataclass
class Desc:
    subj: 'AnalNode'
    aux: Optional['AnalNode']
    desc: 'AnalNode'
    nchks: List['AnalNode']
    modifiers: Optional[List[Tuple[Text, 'AnalNode']]]

    @property
    def subj_spec(self) -> Text:
        return self.subj.spec() if self.subj.is_noun() else '_'

    @property
    def modifier_names(self):
        return [m[0] for m in self.modifiers]

    @property
    def target(self):
        return self.subj

@dataclass
class Behave:
    subj: 'AnalNode'
    obj: 'AnalNode'
    behave: 'AnalNode'
    negative: bool

    @property
    def target(self):
        return self.obj

@dataclass
class Phrase:
    head: 'AnalNode'
    # the key elements are paths
    modifiers: Optional[List[Tuple[Text, 'AnalNode']]]
    @property
    def modifier_names(self):
        return [m[0] for m in self.modifiers]

    @property
    def target(self):
        return self.head

@dataclass
class Nosense:
    node: 'AnalNode'

    @property
    def target(self):
        return self.node

upos_mappings={'ADJ':'a', 'ADV':'r', 'NOUN':'n', 'VERB':'v'}
class AnalNode(NodeMixin, Token):
    lang: Text
    with_trans_opt: bool=False
    position: Tuple[int,int]

    def __init__(self, tok:Optional[WordIntf], parent=None, children=None, **kwargs):
        super(AnalNode, self).__init__(tok)
        self.__dict__.update(kwargs)
        if tok:
            self.__dict__.update(tok.ctx)
        self.parent = parent
        if children:
            self.children = children

    def __repr__(self):
        return _repr(self)

    @cached_property
    def feats_map(self) -> Dict[Text, Any]:
        return extract_feats_map(self.tok.feats, self.doc.engine)

    @cached_property
    def personal_pronoun_repr(self):
        def feat_or(name):
            return self.feats_map[name] if name in self.feats_map else '_'
        if 'Person' in self.feats_map:
            personal = feat_or('Tense') + '_' + feat_or('Person') \
                       + '_' + feat_or('Number')
            return personal
        return ''

    def by_pos(self, pos:Text) -> Tuple['AnalNode', ...]:
        return findall_by_attr(self, name='upos', value=pos)
    @property
    def verbs(self) -> Tuple['AnalNode', ...]:
        return self.by_pos('VERB')

    @property
    def nouns(self) -> Tuple['AnalNode', ...]:
        return self.by_pos('NOUN')
    def is_noun(self) -> bool:
        return self.tok.upos=='NOUN'
    def is_pron(self) -> bool:
        return self.tok.upos in ('PRON', 'DET')

    @property
    def adjectives(self) -> Tuple['AnalNode', ...]:
        return self.by_pos('ADJ')

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

    def has_num(self) -> bool:
        rs= self.find(fn=lambda node: node.dependency_relation in ("nummod")) or \
            self.find(fn=lambda node: node.upos in ("NUM"))
        return len(rs)>0

    def path_to(self, f):
        path = [n.deprel for n in self.walk_to(f)[0]]
        path.reverse()
        return '.'.join(path)

    def draw(self, translate=False):
        """
        >>> from sagas.nlu.anal import build_anal_tree, Doc, AnalNode
        >>> f=build_anal_tree('Η σαλάτα μου έχει τομάτα.', 'el', 'stanza')
        >>> f.draw(True)
        :param translate:
        :return:
        """
        def additional(n):
            addons=[n.lemma]
            if n.upos=='VERB':
                if n.personal_pronoun_repr:
                    addons.append(n.personal_pronoun_repr)
            if n.dependency_relation != 'punct':
                if translate:
                    from sagas.nlu.translator import get_contrast
                    addons.append(get_contrast(n.text, n.lang))
            return '; '.join(addons)
        print(RenderTree(self, style=AsciiStyle()).by_attr(
            lambda n: f"{n.dependency_relation}: {n.text} "
                      f"({additional(n)}, {n.upos.lower()})"))

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
            w, lang=self.word, self.lang
        pos=self.get_pos(pos)
        return predicate(cat, w, lang, pos)

    def get_pos(self, pos='~'):
        return self.pos_abbr if pos == '~' else pos
    @property
    def deprel(self):
        return self.tok.dependency_relation

    @cached_property
    def axis(self):
        from sagas.nlu.translator import trans_axis
        t=self.tok
        word=t.text if t.upos.lower() in ['adj'] else t.lemma
        return trans_axis(word, self.lang, self.tok.upos)

    @staticmethod
    def translit_text(text, lang) -> Text:
        from sagas.nlu.transliterations import translits
        if translits.is_available_lang(lang):
            return translits.translit(text, lang)
        return text

    @staticmethod
    def translate_text(text:Text, source:Text, target:Text='en', cache=True) -> Text:
        """
        >>> AnalNode.translate_text('σαλάτα', 'el', 'en', cache=False)
        """
        from sagas.nlu.translator import translate_try
        options = {'get_pronounce', 'disable_correct'}
        if not cache:
            options.add('disable_cache')
        res_t, _ = translate_try(text, source=source,
                                 target=target,
                                 options=options)
        return res_t

    @cached_property
    def translit(self) -> Text:
        return AnalNode.translit_text(self.tok.text, self.lang)

    @cached_property
    def translit_chunk(self) -> Text:
        return AnalNode.translit_text(self.chunk, self.lang)

    @cached_property
    def translate_chunk(self) -> Text:
        return AnalNode.translate_text(self.chunk, self.lang)

    @cached_property
    def translate(self) -> Text:
        return AnalNode.translate_text(self.tok.text, self.lang)

    def is_interr(self, *interrs) -> bool:
        return self.interr in interrs

    @cached_property
    def interr(self):
        from sagas.nlu.inspectors_dataset import get_interrogative
        return get_interrogative(self.tok.lemma, self.lang)

    def is_negative(self):
        from sagas.nlu.inspectors_dataset import is_negative
        return is_negative(self.word, self.lang)

    @cached_property
    def pred_negative(self):
        ns=self.rels('advmod')
        if not ns:
            return False
        return any([n.is_negative() for n in ns])

    def pred_interr(self, rel, *interrs):
        ns = self.rels(rel)
        if not ns:
            return False
        return any([n.is_interr(*interrs) for n in ns])

    @cached_property
    def pred_enable(self):
        return self.pred_interr('advmod', 'can')

    @cached_property
    def ner(self, provider='rasa_simple'):
        return self.doc.get_index_data(provider, self.tok.index)

    def get_by_index(self, idx) -> 'AnalNode':
        return next((n for n in self.descendants if n.index==idx), None)

    def has_role(self, **roles):
        """
        >>> f.has_role(agent='study|学习')
        :param roles:
        :return:
        """
        return any([st.has_role(**roles) for st in self.sense])

    def inherits(self, base):
        """
        >>> f.inherits('human|人')
        >>> f.nouns[0].with_trans().inherits('language|语言')
        :param base:
        :return:
        """
        return any([st.cat_of(base) for st in self.sense])

    @cached_property
    def sense(self) -> List[SenseTree]:
        """
        >>> f.sense
        :return:
        """
        text=self.axis if self.lang not in ('en', 'zh') else self.tok.lemma
        return get_trees(text)

    def spec_sense(self, pos='~'):
        specs=self.syn_names(pos)
        if specs:
            return get_trees('/'.join(specs))

    @cached_property
    def types(self) -> Set[Text]:
        return {t.name for st in self.sense for t in st.inherits}

    def spec_types(self, pos='~') -> Set[Text]:
        return {t.name for st in self.spec_sense(pos) for t in st.inherits}

    @property
    def word(self):
        return f"{self.tok.text}/{self.tok.lemma}"

    def synsets(self, pos='~'):
        from sagas.nlu.nlu_cli import retrieve_word_info
        rs = retrieve_word_info('get_synsets',
                                self.word, self.lang,
                                self.get_pos(pos))
        if not rs and self.lang!='en':
            rs = retrieve_word_info('get_synsets',
                                    self.axis, 'en',
                                    self.get_pos(pos))
        return rs

    def syn_names(self, pos='~'):
        return [s.split('.')[0] for s in self.synsets(pos)]

    def spec(self, pos='~'):
        from sagas.nlu.utils import get_possible_mean
        return get_possible_mean(self.synsets(pos))

    def chains(self, pos='~'):
        from sagas.nlu.nlu_cli import get_chains
        return get_chains(self.word, self.lang, self.get_pos(pos))

    @cached_property
    def chunk(self):
        from itertools import chain
        from sagas.nlu.constants import delim
        rs = sorted([(c.index, c.text) for c in chain([self], self.descendants)], key=lambda x: x[0])
        return delim(self.lang).join([r[1] for r in rs])

    def as_date(self):
        """
        >>> f=build_anal_tree('2008年12月に上海に行きたいです。', 'ja', 'stanza')
        >>> f.rels('iobj')[0].text, f.rels('iobj')[0].chunk, f.rels('iobj')[0].as_date()
        :return:
        """
        from dateparser.search import search_dates
        from dateparser import parse
        return search_dates(self.chunk, languages=[self.lang]) or \
               parse(self.chunk, languages=[self.lang])

    def dims(self, with_chunk=False):
        from sagas.nlu.inspectors import query_duckling
        resp = query_duckling(self.chunk if with_chunk else self.tok.text, self.lang)
        return resp['data']

    def as_type(self, dim:Text, with_chunk):
        dims = self.dims(with_chunk)
        values = [d for d in dims if d['dim'] == dim]
        return values

    def as_num(self, with_chunk=False):
        vals = self.as_type('number', with_chunk)
        if vals:
            return vals[0]['value']['value']

    @cached_property
    def doc(self):
        for node in self.iter_path_reverse():
            if isinstance(node, Doc):
                return node

    def as_desc(self):
        """
        >>> f=build_anal_tree('Nuestro horario es de nueve a cinco.', 'es', 'stanza')
        >>> desc=f.as_desc()
        >>> desc.subj.text, desc.subj_spec, desc.aux.lemma, desc.desc.as_num()
        :return:
        """
        aux_ls = self.by_pos('AUX')
        if aux_ls:
            aux = aux_ls[0]
            head = aux.parent
            subjs = head.rels('nsubj', 'csubj')
            nchks = head.rels('compound')
            return Desc(subj=node_or(subjs), aux=aux,
                        desc=head, nchks=nchks,
                        modifiers=head.modifiers)

    @cached_property
    def modifiers(self) -> List[Tuple[Text, 'AnalNode']]:
        return [(n.tok.dependency_relation,n) for n in
                self.rels('amod', 'cop', 'advmod')]

    @cached_property
    def subjs(self):
        subjs=self.find(fn=lambda n: n.dependency_relation.endswith('subj'))
        rs=[]
        for node in subjs:
            head = node.parent
            rs.append(Desc(subj=node, aux=None,
                           desc=head,
                           nchks=head.rels('compound'),
                           modifiers=head.modifiers))
        return rs

    def as_noun_phrase(self):
        if self.is_noun():
            modis=s=self.find(fn=lambda n: n.dependency_relation.endswith('mod'))
            return Phrase(head=self,
                          modifiers=[(n.path_to(self),n) for n in modis])

    def as_subj(self):
        rs=self.subjs
        return rs[0] if rs else None

    def as_behave(self):
        """
        Instances for obj:
            * nsubj:pass
                $ se 'the clipboard content has not been changed.'
        :return:
        """
        node_ls=self.by_pos('VERB')
        if node_ls:
            node=node_ls[0]
            return Behave(subj=node_or(node.rels('nsubj', 'csubj')),
                          obj=node_or(node.rels('obj', 'obl', 'nsubj:pass')),
                          behave=node,
                          negative=node.pred_negative,
                          )

    def model(self):
        """
        >>> type(f.model()).__name__
        >>> target=f.model().target
        >>> target.axis, target.types
            ('carpet', {'tool|用具'})

        :return:
        """
        return self.as_behave() or self.as_desc() or \
               self.as_subj() or self.as_noun_phrase() \
               or Nosense(node=self)

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
    doc:SentenceIntf=chunks['doc']
    words = doc.words
    node_map = {word.index: nodecls(word, lang=lang, position=doc.get_position(word.index)) for word in words}
    node_map[0] = Doc(sents=sents, lang=lang, engine=engine, doc=doc)
    tree_root = next(w for w in node_map.values() if w.governor == 0)

    def set_parent(w):
        if isinstance(w, AnalNode):
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
