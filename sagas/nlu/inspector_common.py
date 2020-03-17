from typing import Text, Any, Dict, List, Union, Optional
import abc
from sagas.conf.conf import cf

class Chunk(object):
    def __init__(self, key, children):
        self.key=key
        self.children=children

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        cnt = ' '.join(self.children)
        return f"{self.key}: {cnt}"

class cla_meta_intf():
    @property
    def sents(self):
        raise NotImplementedError('Property not implemented!')

    @property
    def lang(self):
        raise NotImplementedError('Property not implemented!')

class cla_meta(cla_meta_intf):
    def __init__(self, sents:Text, lang:Text):
        self._sents=sents
        self._lang=lang

    @property
    def lang(self):
        return self._lang

    @property
    def sents(self):
        return self._sents

non_spaces=['ja', 'zh']
class Context(cla_meta_intf, object):
    def __init__(self, meta, domains, name=''):
        self.meta=meta
        self.name=name
        self.domains=domains

        # self.chunks = {x[0]: x[4] for x in domains}
        self._chunks = [Chunk(x[0], x[4]) for x in domains]
        # all universal syntactic relations
        self.rels={x[0] for x in domains}
        self._stems = meta['stems']
        if len(self._stems)==0:
            self._stems=[(x[0], x[4]) for x in domains]

        self._lang = meta['lang']
        if self._lang in non_spaces:
            self.delim = ''
        else:
            self.delim = ' '
        self._sents=meta['sents'] if 'sents' in meta else ''
        self.engine=meta['engine'] if 'engine' in meta else cf.engine(self._lang)

        # self.lemmas = {x[0]: x[3] for x in domains}
        # self.words = {x[0]: x[2] for x in domains}
        # Support repeated keys
        keys = {x[0] for x in domains}
        self.indexes={x[0]:x[1] for x in domains}

        grp = lambda p, idx: [x[idx] for x in domains if x[0] == p]
        grp_join = lambda p, idx1, idx2: [f"{x[idx1]}/{x[idx2]}" for x in domains if x[0] == p]
        # self.tokens = {x: grp(x, 2) for x in keys}
        self.tokens = {x: grp_join(x, 2,3) for x in keys}
        self.words = {x: self.delim.join(grp(x, 2)) for x in keys}
        self.lemmas = {x: self.delim.join(grp(x, 3)) for x in keys}

        self.feats = {x[0]: x[5] for x in domains}
        # self.meta['intermedia']={}
        self._results=[]

    def get_word(self, key) -> Text:
        return f"{self.words[key]}/{self.lemmas[key]}"

    @property
    def lang(self):
        return self._lang

    @property
    def sents(self):
        return self._sents

    @property
    def pos(self):
        return self.meta['pos']

    def get_feat_pos(self, part:Text) -> Optional[Text]:
        return self.feats[part][0] if part in self.feats else None

    @property
    def segments(self):
        return self.meta['segments']

    def in_segments(self, lemma) -> (bool, Dict[Text, Any]):
        for seg in self.segments:
            if 'lemmas' in seg and lemma in seg['lemmas']:
                return True, seg
        return False, None

    @property
    def results(self) -> List[Dict[Text, Any]]:
        return self._results

    def add_result(self, inspector:Text, provider:Text, part_name:Text, val, delivery_type='slot'):
        """
        Add result to context
        :param inspector:
        :param provider:
        :param part_name:
        :param val:
        :param delivery_type: default is slot, the other available values is token/sentence
        :return:
        """
        # self._results.append((inspector, provider, part_name, val, delivery_type))
        self._results.append({'inspector':inspector,
                              'provider':provider,
                              'part':part_name,
                              'value':val,
                              'delivery': delivery_type,
                              'pattern': self.name,
                              })

    def put_data(self, key, val):
        if 'intermedia' not in self.meta:
            self.meta['intermedia'] = {}
        self.meta['intermedia'][key]=val

    def get_data(self, key:Text):
        if 'intermedia' not in self.meta:
            self.meta['intermedia'] = {}

        if key not in self.meta['intermedia']:
            return None
        return self.meta['intermedia'][key]

    def get_chunks(self, key:Text) -> List:
        return [c for c in self._chunks if c.key==key]

    def get_stems(self, key:Text) -> List:
        return [c for c in self._stems if c[0]==key]

    def chunk_contains(self, key:Text, val: Union[Text, List]):
        chunks = self.get_chunks(key)
        if isinstance(val, list):
            vals=val
        else:
            vals=[val]

        for v in vals:
            for c in chunks:
                if v in c.children:
                    return True
        return False

    def get_single_chunk_text(self, key:Text):
        chunks=self.get_chunks(key)
        if len(chunks)>0:
            cnt = self.delim.join(chunks[0].children)
            return cnt
        return ''

    def chunk_pieces(self, key:Text, lowercase=False) -> List[Text]:
        chunks = self.get_chunks(key)
        return [self.delim.join(c.children).lower() if lowercase else self.delim.join(c.children) for c in chunks]

    def stem_pieces(self, key:Text) -> List[Text]:
        stems = self.get_stems(key)
        if self.lang in non_spaces:
            delim=''
        else:
            delim=' '
        return [delim.join(c[1]) for c in stems]

# enable_cache=False
class Inspector(object):
    @abc.abstractmethod
    def name(self) -> Text:
        """Unique identifier of this simple inspector."""
        raise NotImplementedError("An inspector must implement a name")

    @property
    def result(self):
        return None

    @property
    def after(self):
        """
        返回True表示这个inspector将在其它inspector全部执行完毕后才执行
        :return:
        """
        return False

    @property
    def when_succ(self):
        """
        返回True表示这个inspector将在其它inspector全部为真的情况下才执行,
        除了标记after=True的inspector之外.
        :return:
        """
        return False

    @abc.abstractmethod
    def run(self, key:Text, ctx:Context) -> bool:
        """
        仅用于继承, check方法会负责调用这个方法
        :param key:
        :param ctx:
        :return:
        """
        raise NotImplementedError("An inspector must implement its run method")

    # def cache_key(self, key):
    #     return "%s.%s"%(self.name(), key)

    def check(self, key:Text, ctx:Context) -> bool:
        """
        Api method
        :param key:
        :param ctx:
        :return:
        """
        # if enable_cache:
        #     cache = ctx.get_data(self.cache_key(key))
        #     if cache is not None:
        #         return cache
        #
        #     result=self.run(key, ctx)
        #     ctx.put_data(self.cache_key(key), result)
        #     return result
        # else:
        return self.run(key, ctx)

    def infer(self, insps:List, insp_pairs:Dict[Text, Any]):
        pass

    def __str__(self):
        return "Inspector('{}')".format(self.name())

    def __repr__(self):
        return self.__str__()

