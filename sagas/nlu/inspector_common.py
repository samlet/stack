class Chunk(object):
    def __init__(self, key, children):
        self.key=key
        self.children=children

non_spaces=['ja', 'zh']
class Context(object):
    def __init__(self, meta, domains, name=''):
        self.meta=meta
        self.name=name
        # self.chunks = {x[0]: x[4] for x in domains}
        self._chunks = [Chunk(x[0], x[4]) for x in domains]
        self._stems = meta['stems']
        if len(self._stems)==0:
            self._stems=[(x[0], x[4]) for x in domains]

        self.lemmas = {x[0]: x[3] for x in domains}
        self.feats = {x[0]: x[5] for x in domains}
        # self.meta['intermedia']={}
        self.lang = meta['lang']

        self._results=[]

    @property
    def results(self):
        return self._results
    def add_result(self, inspector, provider, part_name, val):
        self._results.append((inspector, provider, part_name, val))

    def put_data(self, key, val):
        if 'intermedia' not in self.meta:
            self.meta['intermedia'] = {}
        self.meta['intermedia'][key]=val

    def get_data(self, key):
        if 'intermedia' not in self.meta:
            self.meta['intermedia'] = {}

        if key not in self.meta['intermedia']:
            return None
        return self.meta['intermedia'][key]

    def get_chunks(self, key):
        return [c for c in self._chunks if c.key==key]

    def get_stems(self, key):
        return [c for c in self._stems if c[0]==key]

    def chunk_contains(self, key, val):
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

    def get_single_chunk_text(self, key):
        chunks=self.get_chunks(key)
        if len(chunks)>0:
            cnt = ' '.join(chunks[0].children)
            return cnt
        return ''

    def chunk_pieces(self, key):
        chunks = self.get_chunks(key)
        if self.lang in non_spaces:
            delim=''
        else:
            delim=' '
        return [delim.join(c.children) for c in chunks]

    def stem_pieces(self, key):
        stems = self.get_stems(key)
        if self.lang in non_spaces:
            delim=''
        else:
            delim=' '
        return [delim.join(c[1]) for c in stems]

enable_cache=False
class Inspector(object):
    def name(self):
        # type: () -> Text
        """Unique identifier of this simple inspector."""

        raise NotImplementedError("An inspector must implement a name")

    @property
    def result(self):
        return None

    def run(self, key, ctx:Context):
        """
        仅用于继承, check方法会负责调用这个方法
        :param key:
        :param ctx:
        :return:
        """
        raise NotImplementedError("An inspector must implement its run method")

    def cache_key(self, key):
        return "%s.%s"%(self.name(), key)

    def check(self, key, ctx:Context):
        """
        Api method
        :param key:
        :param ctx:
        :return:
        """
        if enable_cache:
            cache = ctx.get_data(self.cache_key(key))
            if cache is not None:
                return cache

            result=self.run(key, ctx)
            ctx.put_data(self.cache_key(key), result)
            return result
        else:
            return self.run(key, ctx)

    def __str__(self):
        return "Inspector('{}')".format(self.name())

