class Chunk(object):
    def __init__(self, key, children):
        self.key=key
        self.children=children

class Context(object):
    def __init__(self, meta, domains):
        self.meta=meta
        # self.chunks = {x[0]: x[4] for x in domains}
        self._chunks = [Chunk(x[0], x[4]) for x in domains]
        self.lemmas = {x[0]: x[3] for x in domains}
        self.feats = {x[0]: x[5] for x in domains}

    def get_chunks(self, key):
        return [c for c in self._chunks if c.key==key]

    def chunk_contains(self, key, val):
        chunks = self.get_chunks(key)
        for c in chunks:
            if val in c.children:
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
        return [' '.join(c.children) for c in chunks]

class Inspector(object):
    def name(self):
        # type: () -> Text
        """Unique identifier of this simple inspector."""

        raise NotImplementedError("An inspector must implement a name")

    def run(self, key, ctx:Context):
        raise NotImplementedError("An inspector must implement its run method")

    def __str__(self):
        return "Inspector('{}')".format(self.name())

