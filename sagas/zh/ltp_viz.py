class LtpViz(object):
    """
    from sagas.zh.ltp_procs import LtpProcs
    ltp=LtpProcs()
    ana=lambda sents: LtpViz(ltp).deps(sents)
    """
    def __init__(self, ltp=None):
        from graphviz import Digraph
        from sagas.zh.ltp_procs import LtpProcs

        if ltp is None:
            ltp = LtpProcs()
        self.ltp = ltp
        self.f = Digraph('deps', filename='deps.gv')
        self.f.attr(rankdir='LR', size='6,4')
        self.f.attr('node', shape='circle')

    def deps(self, sentence):
        words = self.ltp.segmentor.segment(sentence)
        postags = self.ltp.postagger.postag(words)
        arcs = self.ltp.parser.parse(words, postags)
        roles = self.ltp.labeller.label(words, postags, arcs)
        netags = self.ltp.recognizer.recognize(words, postags)

        for i in range(len(words)):
            a = words[int(arcs[i].head) - 1]
            print("%s --> %s|%s|%s|%s" % (a, words[i], \
                                          arcs[i].relation, postags[i], netags[i]))
            self.f.edge(a, words[i], label=arcs[i].relation.lower())
        return self.f


