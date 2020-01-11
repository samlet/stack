from sagas.nlu.corenlp_helper import get_nlp
from sagas.nlu.env import sa_env
import sagas.tracker_fn as tc


class EnhancedViz(object):
    """
    from sagas.nlu.uni_viz import EnhancedViz
    cv = EnhancedViz(shape='egg', size='8,5', fontsize=20)
    cv.analyse_doc(doc, None)
    """
    def __init__(self, shape='egg', size='8,5', fontsize=0, enable_node_pos=False, translit_lang=None):
        from graphviz import Digraph
        self.f = Digraph('deps', filename='deps.gv')
        self.f.attr(rankdir='LR', size=size)
        # font 'Calibri' support Arabic text
        self.f.attr('node', shape=shape, fontname='Calibri')
        if fontsize != 0:
            self.f.attr(fontsize=str(fontsize))
        self.enable_node_pos=enable_node_pos
        self.translit_lang=translit_lang

    def fix_console_label(self, label):
        if self.translit_lang is not None and self.translit_lang in ('ja'):
            from sagas.nlu.transliterations import translits
            return translits.trans_icu(label)
        return label

    def print_dependencies(self, doc, segs, node_maps, verbose=False):
        for dep_edge in doc.dependencies:
            if verbose:
                tc.info((dep_edge[2].text, dep_edge[0].index, dep_edge[1]))
            # head = int(dep_edge[0].index)
            # governor-id is index in words list + 1
            rel = dep_edge[1]

            if rel.endswith('comp'):
                self.f.attr('edge', style='dashed')
            else:
                self.f.attr('edge', style='solid')

            head = int(dep_edge[0].index) - 1
            node_text = node_maps[dep_edge[2].text]

            if head==-1:
                # print("%s's head is root %s"%(node_text, segs[head]))
                head_node='ROOT'
            else:
                head_node=segs[head]

            self.f.edge(head_node, node_text, label=self.fix_console_label(rel),
                        fontsize='11', fontname='Calibri')
            # self.f.edge(dep_edge[2].text, segs[head], label=dep_edge[1])

    def analyse(self, sents, nlp, node_maps=None):
        doc = nlp(sents)
        return self.analyse_doc(doc, node_maps)

    def default_node(self):
        self.f.attr('node', style='solid', color='black')

    def analyse_doc(self, sentence, node_maps=None, console=True):
        from sagas.nlu.uni_intf import sub_comps
        import unicodedata

        segs = []
        # omit {word.feats}
        if console:
            tc.info(*[f'index: {word.index}\ttext: {word.text+" "}\tlemma: {word.lemma}\tupos: {word.upos}\txpos: {word.xpos}' for word in sentence.words], sep='\n')
        else:
            # from IPython.display import display
            import sagas
            df=sagas.to_df([(word.index, word.text, word.lemma, word.upos, word.xpos) for word in sentence.words],
                           ['index', 'text', 'lemma', 'upos', 'xpos'])
            tc.dfs(df)

        def translit_chunk(chunk:str, lang):
            from sagas.nlu.transliterations import translits
            # if upos=='PUNCT':
            #     return chunk
            if chunk.strip() in (',','.',';','?','!'):
                return chunk
            # if lang in ('ko', 'ja', 'fa', 'hi', 'ar'):
            if translits.is_available_lang(lang):
                if sa_env.runtime!='default':
                    return word.text+'\n'+translits.translit(chunk, lang)
                return translits.translit(chunk, lang)
            return chunk

        if node_maps is None:
            node_maps = {}
            for word in sentence.words:
                pos_attrs=f"({word.upos.lower()}, {word.xpos.lower()})"
                node_text=word.text if self.translit_lang is None or word.upos=='PUNCT' \
                    else translit_chunk(word.text, self.translit_lang)
                # node_text=unicodedata.normalize('NFKC', node_text) if word.upos=='PUNCT' else node_text
                norm=lambda t: unicodedata.normalize('NFKC', t).encode('ascii', 'ignore').decode("utf-8")
                node_text = norm(node_text) if word.upos == 'PUNCT' else node_text
                if node_text=='':
                    node_text='_'
                # verbose
                if word.text!=node_text:
                    print('# ', f"{word.text} -> {node_text}")
                node_maps[word.text] = node_text if not self.enable_node_pos else f"{node_text}\\n{pos_attrs}"

                # self.f.attr(color='black')
        prop_sets = {'VERB': lambda f: f.attr('node', style='filled', color='lightgrey'),
                     'PRON': lambda f: f.attr('node', style='dashed', color='red'),
                     'AUX': lambda f: f.attr('node', style='dashed', color='green'),
                     'NOUN': lambda f: f.attr('node', style='solid', color='blue'),
                     }
        # sentence = doc.sentences[0]
        for word in sentence.words:
            rel = word.dependency_relation
            if rel in sub_comps:
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
            # print(f"{word.text} -> {rel}, {word.governor}, {head}")
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
        tc.info('%s(%s)' % (r['type'], r['lemma']))
        tc.dfs(df)
        # display(df)
        print_stem_chunks(r)

    cv = EnhancedViz(shape='egg', size='8,5', fontsize=20)
    return cv.analyse_doc(doc, None)

