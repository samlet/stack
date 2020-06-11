from typing import Text, Any, Dict, List, Union, Optional, Tuple, Set
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from sagas.nlu.anal_data_types import path_, pos_, ConstType, PredCond, behave_, desc_, phrase_, _, rel_, Carrier, ref_, \
    ExtensionHolder

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
from sagas.conf.conf import cf
import pandas as pd
import logging

logger = logging.getLogger(__name__)

@dataclass_json
@dataclass
class SemanticRole:
    rel: str
    index: int
    text: str
    lemma: str
    children: List[Text]
    features: List[Text]

@dataclass_json
@dataclass
class Predict:
    type: str
    lemma: str
    index: int
    phonetic: str
    word: str
    rel: str
    governor: int
    pos: str
    domains: List[SemanticRole]

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
    _predicts: List[Any]=[]

    def __init__(self, parent=None, children=None, **kwargs):
        self.__dict__.update(kwargs)
        self.parent = parent
        if children:
            self.children = children
        self._ = self.extens = ExtensionHolder()

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

    @property
    def predict_domains_df(self) -> List[pd.DataFrame]:
        import sagas
        if not self._predicts:
            return []

        dfs=[]
        for r in self._predicts:
            df = sagas.to_df(r['domains'], ['rel', 'index', 'text',
                                            'lemma', 'children', 'features'])
            dfs.append(df)
        return dfs

    @cached_property
    def predicts(self):
        import sagas
        import sagas.util.pandas_helper as ph
        preds = []
        for p in self._predicts:
            pred = Predict(type=p['type'], lemma=p['lemma'], index=p['index'],
                           phonetic=p['phonetic'], word=p['word'],
                           rel=p['rel'], governor=p['governor'],
                           pos=p['pos'], domains=[]
                           )
            df = sagas.to_df(p['domains'], ['rel', 'index', 'text', 'lemma',
                                            'children', 'features'])

            for e in ph.to_json(df):
                pred.domains.append(SemanticRole(rel=e['rel'], index=e['index'], text=e['text'],
                                                 lemma=e['lemma'], children=e['children'],
                                                 features=e['features']
                                                 ))
            preds.append(pred)
        return preds

    @property
    def root(self):
        return self.children[0]

class Token(object):
    def __init__(self, tok:Optional[WordIntf]):
        self.tok=tok  # readonly
        self.name=tok.dependency_relation if tok is not None else '_'

def node_or(nodels):
    return nodels[0] if nodels else None
def node_desc(n:'AnalNode'):
    return f"{n.tok.lemma}({n.deprel})" if n else '_'

MatchResult=Tuple[bool, List[Tuple[str, bool]]]

def match_and_rep(a,b,c, flags, head) -> MatchResult:
    chk_rep = []
    for n, chk, op in zip(a, b, c):
        if chk == _:
            r = True
        elif n is not None:
            r = n.match(chk)
        else:
            # 如果位置标记不是通配符, 值也为空时, 则匹配失败;
            # 特殊情况是"_2 << _"这样的形式, 虽然是通配符, 但如果该位置没有结点值,
            # 也会匹配失败, 因为无法提取指定的结点. 所以当可能有值缺失的时候, 可以用两个分支,
            # 分别匹配该位置有值/无值两种情况.
            r = False
        chk_rep.append((op, r))

    for flag in flags:
        node = head / flag
        r = node.match(flag.cond) if node else False
        chk_rep.append((str(flag), r))

    return all([r for op, r in chk_rep]), chk_rep

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

    def match(self, pred:desc_) -> MatchResult:
        a=(self.subj, self.desc, self.aux)
        b=(pred.subj, pred.desc, pred.aux)
        c = ('subj', 'desc', 'aux')
        return match_and_rep(a,b,c, pred.flags, self.desc)

@dataclass
class Behave:
    subj: 'AnalNode'
    obj: 'AnalNode'
    iobj: 'AnalNode'
    behave: 'AnalNode'
    negative: bool

    @property
    def target(self):
        return self.obj

    def match(self, pred:behave_) -> MatchResult:
        a=(self.subj, self.behave, self.obj, self.iobj)
        b=(pred.subj, pred.behave, pred.obj, pred.iobj)
        c = ('subj', 'behave', 'obj', 'iobj')
        return match_and_rep(a,b,c, pred.flags, self.behave)

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

    def match(self, pred:phrase_) -> MatchResult:
        a=[self.head]
        b=[pred.head]
        c = ['head']
        return match_and_rep(a,b,c, pred.flags, self.head)

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

        self._ = self.extens = ExtensionHolder()

    def __repr__(self):
        return _repr(self)

    def set_extension(self, attr_name, attr_val):
        """
        >>> t.set_extension('x','hello')
        >>> t._.x
        :param attr_name:
        :param attr_val:
        :return:
        """
        self._.attrs[attr_name] = attr_val

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

    def rels(self, *args, level=2) -> Tuple['AnalNode', ...]:
        return findall(self, filter_=lambda n: n.dependency_relation in args, maxlevel=level)

    def rels_by_order(self, *args, level=2) -> Optional['AnalNode']:
        for a in args:
            rs=findall(self, filter_=lambda n: n.dependency_relation==a, maxlevel=level)
            if rs:
                return rs[0]

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

    def find(self, fn, level=None) -> Tuple:
        """
        >>> f.find(fn=lambda node: node.dependency_relation in ("obj"))
        :param fn:
        :return:
        """
        return findall(self, filter_=fn, maxlevel=level)

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
            addons=[str(n.index), n.lemma]
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
        def try_trans():
            from sagas.nlu.translator import trans_axis
            for word in (self.text, self.lemma):
                rt=trans_axis(word, self.lang, self.tok.upos)
                if rt:
                    st=get_trees(rt, self.pos_abbr)
                    if st:
                        return st
            return []
        if self.lang in ('en', 'zh'):
            return get_trees(self.tok.lemma, self.pos_abbr)
        else:
            return try_trans()

    def spec_sense(self, pos='~'):
        specs=self.syn_names(pos)
        if specs:
            return get_trees('/'.join(specs), self.get_pos(pos))

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
            modis=self.find(fn=lambda n: n.dependency_relation.endswith('mod'))
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
            return Behave(subj=node.rels_by_order('nsubj', 'csubj'),
                          obj=node.rels_by_order('obj', 'ccomp', 'xcomp', 'nsubj:pass', 'obl'),
                          iobj=node.rels_by_order('iobj'),
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

    def __floordiv__(self, other):
        """ (f//'obj')[0].lemma,
        """
        if isinstance(other, str):
            return self.rels(other)
        elif isinstance(other, rel_):
            return self.rels(other.val)
        elif isinstance(other, path_):
            return self.resolve_rels(other.val)
        elif isinstance(other, pos_):
            return self.by_pos(other.val.upper())

    def __truediv__(self, other):
        """ (f/'nsubj').lemma,
            (f/pos_('pron')).text
        """
        if isinstance(other, int):
            return self.get_by_index(other)

        rs= self.__floordiv__(other)
        return rs[0] if rs else None

    def match(self, pred: PredCond) -> bool:
        ret, _=self.do_match(pred)
        return ret

    def do_match(self, pred:PredCond) -> Tuple[bool, Any]:
        """
        位置参数值的解释途径, 默认是spec, 可包含'/', 包含了'|'则为sense,
        包含了':'则为角色, 以'$'开始则为interr, 特别前辍也与角色一样使用':',
        比如pos. 也可以用结构类, 比如pos_, 就可以不用':'前辍了.
        如果是'或'条件, 使用';'分隔多个值, 值可以是spec/sense/roles/interr/pos.
        如果是'与'条件, 则以'+'作为起始字符, 值以';'分隔.
        如果使用了抽取符(_1,_2,..), 则抽取对应位置的node,
        如果是对应位置是behave_, desc_等类型, 则抽取的为对应的Behave, Desc结构.

        :param pred:
        :return:
        """
        result_op=any

        if isinstance(pred, Carrier):
            carrier=pred
            pred=carrier.take_req()
            logger.debug(f"found a carrier, pred is {pred}")
            carrier.put_resp(self)
        else:
            carrier=None

        def do_op(op):
            if op:
                r,t=op.match(pred)
                logger.debug(t)
                if carrier is not None:
                    carrier.put_resp(op)
                return r, op
            return False, None

        if isinstance(pred, ConstType):
            vals=[str(pred)]
        elif isinstance(pred, str):
            if pred[0]=='+':
                pred=pred[1:]
                result_op=all
            vals=[s.strip() for s in pred.split(';')]
        elif isinstance(pred, behave_):
            return do_op(self.as_behave())
        elif isinstance(pred, desc_):
            # logger.debug(f"pred desc: {pred}")
            op=self.as_desc()
            op=self.as_subj() if not op else op
            return do_op(op)
        elif isinstance(pred, phrase_):
            op=self.as_noun_phrase()
            return do_op(op)
        else:
            return False, None

        results=[]
        for val in vals:
            r=False
            if val=='_':
                r= True

            elif ':' in val:
                # roles
                k,v=val.split(':')
                item_name, item_val=k.strip(), v.strip()
                if item_name =='pos':
                    r=self.tok.upos==item_val.upper()
                elif item_name=='term':
                    r=self.is_term(item_val)
                else:
                    r=self.has_role(**{item_name:item_val})
            elif '|' in val:
                # inherits
                r= self.inherits(val)
            elif val.startswith('$'):
                r= self.is_interr(val[1:])

            else:
                r= self.is_cat(val)
            results.append(r)

        return result_op(results), self

    def __eq__(self, cond):
        return self.match(cond)

    @cached_property
    def ref(self) -> Tuple[Optional[Text], Optional[Text]]:
        from sagas.nlu.anal_conf import AnalConf
        if self.tok.term:
            return AnalConf.split_label(self.tok.term['term'])
        return None, None

    def is_term(self, term_name) -> bool:
        return term_name==self.ref[0]

    @property
    def links(self):
        from sagas.nlu.warehouse import warehouse as wh
        if self.is_term('ref'):
            return wh//ref_(self.ref[1])
        return []

# @cached(cache={}) ->  因为tree-nodes是可以修改的有状态的, 所以不用cached,
#                       但anal-node.tok引用的是只读的文档结点.
def build_anal_tree(sents:Text, lang:Text, engine:Text,
                    nodecls=None, docimpl=None):
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
    from sagas.nlu.uni_remote import dep_parse
    from sagas.nlu.utils import fix_sents

    sents=fix_sents(sents, lang)
    # doc is SentenceIntf
    doc, resp = dep_parse(sents, lang=lang, engine=engine, pipelines=['predicts'],
                          doc_impl=docimpl)
    predicts=resp['predicts'] if resp and 'predicts' in resp else []
    return from_doc(doc, lang, engine, nodecls, predicts)

def from_doc(doc:SentenceIntf, lang, engine, nodecls=None, predicts=None):
    words = doc.words
    if nodecls is None:
        nodecls = cf.extensions('anal', lang)
    node_map = {word.index: nodecls(word, lang=lang, position=doc.get_position(word.index)) for word in words}
    doccls = cf.extensions('anal.doc', lang)
    node_map[0] = doccls(sents=doc.sents, lang=lang, engine=engine,
                         doc=doc, _predicts=predicts if predicts else [])
    tree_root = next(w for w in node_map.values() if w.governor == 0)

    def set_parent(w):
        if isinstance(w, AnalNode):
            w.parent = node_map[w.tok.governor]

    list(map(set_parent, node_map.values()))

    # process doc pipelines
    for pipe in cf.pipelines(lang):
        p = pipe()
        if p.support_langs == '*' or lang in p.support_langs:
            p.process(tree_root.doc)
    return tree_root

def generic_paths(f:AnalNode):
    from itertools import chain
    subjs=f.resolve_rels('*subj')
    start=subjs[0] if subjs else f
    for n in chain(f.nouns, f.adjectives):
        start.walk_to(n, verbose=True)

class AnalDelegator(object):
    """
    >>> from sagas.nlu.anal import delegator
    >>> f=delegator.es('Nuestro horario es de nueve a cinco.')
    >>> f.draw()
    """
    def __getattr__(self, lang):
        return lambda sents: build_anal_tree(sents, lang, cf.engine(lang))

    def f(self, sents, lang):
        return build_anal_tree(sents, lang, cf.engine(lang))

    def doc(self, lang):
        doccls = cf.extensions('anal.doc', lang)
        return doccls

    def node(self, lang):
        return cf.extensions('anal', lang)

delegator=AnalDelegator()

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
