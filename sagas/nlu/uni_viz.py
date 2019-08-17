from sagas.nlu.corenlp_helper import get_nlp

class EnhancedViz(object):
    """
    from sagas.nlu.uni_viz import EnhancedViz
    cv = EnhancedViz(shape='egg', size='8,5', fontsize=20)
    cv.analyse_doc(doc, None)
    """
    def __init__(self, shape='egg', size='8,5', fontsize=0):
        from graphviz import Digraph
        self.f = Digraph('deps', filename='deps.gv')
        self.f.attr(rankdir='LR', size=size)
        # font 'Calibri' support Arabic text
        self.f.attr('node', shape=shape, fontname='Calibri')
        if fontsize != 0:
            self.f.attr(fontsize=str(fontsize))

    def print_dependencies(self, doc, segs, node_maps, file=None):
        for dep_edge in doc.dependencies:
            print((dep_edge[2].text, dep_edge[0].index, dep_edge[1]), file=file)
            # head = int(dep_edge[0].index)
            # governor-id is index in words list + 1
            rel = dep_edge[1]

            if rel.endswith('comp'):
                self.f.attr('edge', style='dashed')
            else:
                self.f.attr('edge', style='filled')

            head = int(dep_edge[0].index) - 1
            node_text = node_maps[dep_edge[2].text]

            if head==-1:
                # print("%s's head is root %s"%(node_text, segs[head]))
                head_node='ROOT'
            else:
                head_node=segs[head]

            self.f.edge(head_node, node_text, label=rel, fontsize='11', fontname='Calibri')
            # self.f.edge(dep_edge[2].text, segs[head], label=dep_edge[1])

    def analyse(self, sents, nlp, node_maps=None):
        doc = nlp(sents)
        return self.analyse_doc(doc, node_maps)

    def default_node(self):
        self.f.attr('node', style='solid', color='black')

    def analyse_doc(self, sentence, node_maps=None):
        segs = []
        # omit {word.feats}
        print(*[f'index: {word.index}\ttext: {word.text+" "}\tlemma: {word.lemma}\tupos: {word.upos}\txpos: {word.xpos}' for word in sentence.words], sep='\n')
        if node_maps is None:
            node_maps = {}
            for word in sentence.words:
                node_maps[word.text] = word.text

                # self.f.attr(color='black')
        prop_sets = {'VERB': lambda f: f.attr('node', style='filled', color='lightgrey'),
                     'PRON': lambda f: f.attr('node', style='dashed', color='red'),
                     'AUX': lambda f: f.attr('node', style='dashed', color='green'),
                     'NOUN': lambda f: f.attr('node', style='solid', color='blue'),
                     }
        # sentence = doc.sentences[0]
        for word in sentence.words:
            rel = word.dependency_relation

            # for zh
            if rel in ['adv', 'coo', 'vob', 'att']:
                if word.upos == 'VERB':
                    self.f.attr('node', style='filled', color='antiquewhite')
                elif word.upos in prop_sets:
                    prop_sets[word.upos](self.f)
                else:
                    self.default_node()

            # for all languages
            elif rel.endswith('comp'):
                self.f.attr('node', style='filled', color='antiquewhite')
            elif word.upos in prop_sets:
                prop_sets[word.upos](self.f)
            else:
                self.default_node()

            head = ''
            if word.governor == 0:
                head = '_root_'
            else:
                head_word = sentence.words[word.governor - 1]
                head = head_word.text
            print(f"{word.text} -> {rel}, {word.governor}, {head}")
            self.f.node(node_maps[word.text])
            segs.append(node_maps[word.text])

        # self.f.node_attr.update(color='black')
        self.default_node()
        self.print_dependencies(sentence, segs, node_maps)
        return self.f


def viz(sents, lang='fr'):
    """
    viz("Tu as choisi laquelle tu vas manger ?")
    viz('I am a student', 'en')
    viz('彼らは3月に訪ねて来ます。', 'ja')
    :param sents:
    :param lang:
    :return:
    """
    nlp = get_nlp(lang)
    doc = nlp(sents)
    cv = EnhancedViz(shape='egg', size='8,5', fontsize=20)
    sentence = doc.sentences[0]
    return cv.analyse_doc(sentence, None)

def universal_viz(intp, sents):
    from sagas.nlu.corenlp_parser import get_chunks
    from sagas.tool.misc import print_stem_chunks
    import sagas

    doc = intp(sents)
    doc.build_dependencies()
    # print(doc.dependencies)
    rs = get_chunks(doc)
    # print(rs)
    for r in rs:
        df = sagas.to_df(r['domains'], ['rel', 'index', 'text', 'lemma', 'children', 'features'])
        print('%s(%s)' % (r['type'], r['lemma']))
        sagas.print_df(df)
        # display(df)
        print_stem_chunks(r)

    cv = EnhancedViz(shape='egg', size='8,5', fontsize=20)
    return cv.analyse_doc(doc, None)

