from nltk.corpus import wordnet as wn

hypo = lambda s: s.hyponyms()
hyper = lambda s: s.hypernyms()

class WordNetViz(object):
    """
    >>> wnet=WordNetViz()
    >>> wnet.get_hyper('apple', 'n')
    """
    def __init__(self, shape='egg', size='8,8', fontsize=0):
        from graphviz import Digraph, Graph
        self.f = Digraph('deps', filename='deps.gv')
        # self.f = Graph('G', filename='process.gv')
        self.f.attr(rankdir='LR', size=size)
        # font 'Calibri' support Arabic text
        self.f.attr('node', shape=shape, fontname='Calibri')
        if fontsize != 0:
            self.f.attr(fontsize=str(fontsize))

    def add_tuples(self, tuples):
        for t in tuples:
            self.f.edge(t[0], t[1], label='_')
        return self.f

    def get_inherited(self, word, pos, clo, top=3, max=4):
        sets = wn.synsets(word, pos)
        print(sets)
        for s in sets[:top]:
            rs = [s.name()]
            ss = list(s.closure(clo))
            # for w in ss[:top]:
            for w in ss:
                rs.extend([w.name() for w in ss])

            count = len(rs) - 1
            if max != -1 and count > max:
                count = max
            print(', '.join(rs)[:40], '...')
            for n in range(count):
                self.f.edge(rs[n], rs[n + 1], label='_')
        return self.f

    def get_hyper(self, word, pos):
        return self.get_inherited(word, pos, hyper)

