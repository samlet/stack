import stanfordnlp
import pandas as pd
from sagas.conf.conf import cf

model_dir=f'{cf.conf_dir}/ai/corenlp'


def load_model(lang,treebank):
    return stanfordnlp.Pipeline(models_dir=model_dir,
                                lang=lang,
                                treebank=treebank)

langs_models={}
def get_nlp(lang):
    if lang not in langs_models:
        from sagas.nlu.treebanks import treebanks
        bank=treebanks.query(lang)
        if bank is None:
            raise Exception('Cannot find treebank for language {}'.format(lang))
        langs_models[lang]=load_model(bank['name'], bank['model'])
    return langs_models[lang]

#extract lemma
def extract_lemma(doc):
    """
    from sagas.nlu.corenlp_helper import langs, extract_lemma, extract_pos
    sents='Apple is looking at buying U.K. startup for $1 billion'
    nlp=langs['en']()
    doc = nlp(sents)
    extract_lemma(doc)

    :param doc:
    :return:
    """
    parsed_text = {'word':[], 'lemma':[]}
    for sent in doc.sentences:
        for wrd in sent.words:
            #extract text and lemma
            parsed_text['word'].append(wrd.text)
            parsed_text['lemma'].append(wrd.lemma)
    #return a dataframe
    return pd.DataFrame(parsed_text)

#dictionary that contains pos tags and their explanations
pos_dict = {
'CC': 'coordinating conjunction','CD': 'cardinal digit','DT': 'determiner',
'EX': 'existential there (like: \"there is\" ... think of it like \"there exists\")',
'FW': 'foreign word','IN':  'preposition/subordinating conjunction','JJ': 'adjective \'big\'',
'JJR': 'adjective, comparative \'bigger\'','JJS': 'adjective, superlative \'biggest\'',
'LS': 'list marker 1)','MD': 'modal could, will','NN': 'noun, singular \'desk\'',
'NNS': 'noun plural \'desks\'','NNP': 'proper noun, singular \'Harrison\'',
'NNPS': 'proper noun, plural \'Americans\'','PDT': 'predeterminer \'all the kids\'',
'POS': 'possessive ending parent\'s','PRP': 'personal pronoun I, he, she',
'PRP$': 'possessive pronoun my, his, hers','RB': 'adverb very, silently,',
'RBR': 'adverb, comparative better','RBS': 'adverb, superlative best',
'RP': 'particle give up','TO': 'to go \'to\' the store.','UH': 'interjection errrrrrrrm',
'VB': 'verb, base form take','VBD': 'verb, past tense took',
'VBG': 'verb, gerund/present participle taking','VBN': 'verb, past participle taken',
'VBP': 'verb, sing. present, non-3d take','VBZ': 'verb, 3rd person sing. present takes',
'WDT': 'wh-determiner which','WP': 'wh-pronoun who, what','WP$': 'possessive wh-pronoun whose',
'WRB': 'wh-abverb where, when','QF' : 'quantifier, bahut, thoda, kam (Hindi)','VM' : 'main verb',
'PSP' : 'postposition, common in indian langs','DEM' : 'demonstrative, common in indian langs'
}

#extract parts of speech
def extract_pos(doc):
    parsed_text = {'word':[], 'pos':[], 'exp':[]}
    for sent in doc.sentences:
        for wrd in sent.words:
            if wrd.pos in pos_dict.keys():
                pos_exp = pos_dict[wrd.pos]
            else:
                pos_exp = 'NA'
            parsed_text['word'].append(wrd.text)
            parsed_text['pos'].append(wrd.pos)
            parsed_text['exp'].append(pos_exp)
    #return a dataframe of pos and text
    return pd.DataFrame(parsed_text)


class CoreNlpViz(object):
    """
    ana=lambda sents: CoreNlpViz(shape='ellipse', size='8,5', fontsize=20).analyse(sents, get_nlp('ar'),
                                       get_word_map('ar','en', sents))
    """
    def __init__(self, shape='egg', size='8,5', fontsize=0):
        from graphviz import Digraph
        self.f = Digraph('deps', filename='deps.gv')
        self.f.attr(rankdir='LR', size=size)
        # font 'Calibri' support Arabic text
        self.f.attr('node', shape=shape, fontname='Calibri')
        if fontsize!=0:
            self.f.attr(fontsize=str(fontsize))

    def print_dependencies(self, doc, segs, node_maps, file=None):
        for dep_edge in doc.dependencies:
            print((dep_edge[2].text, dep_edge[0].index, dep_edge[1]), file=file)
            # head = int(dep_edge[0].index)
            # governor-id is index in words list + 1
            head = int(dep_edge[0].index)-1
            node_text=node_maps[dep_edge[2].text]
            if head==-1:
                # print("%s's head is root %s"%(node_text, segs[head]))
                head_node='ROOT'
            else:
                head_node=segs[head]
            self.f.edge(head_node, node_text, label=dep_edge[1])
            # self.f.edge(dep_edge[2].text, segs[head], label=dep_edge[1])

    def analyse(self, sents, nlp, node_maps=None):
        doc = nlp(sents)
        return self.analyse_doc(doc, node_maps)

    def analyse_doc(self, doc, node_maps=None):
        """
        Usage:

            from sagas.nlu.corenlp_helper import CoreNlpViz, langs, nlp_en, nlp_fr
            nlp=nlp_en() # or nlp=langs['de']()
            CoreNlpViz().analyse('how difficult can teaching children be', nlp)

        :param sents:
        :param nlp:
        :return:
        """
        segs = []
        print(*[f'text: {word.text+" "}\tlemma: {word.lemma}\tupos: {word.upos}\txpos: {word.xpos}' for sent in
                doc.sentences for word in sent.words], sep='\n')
        if node_maps is None:
            node_maps={}
            for word in doc.sentences[0].words:
                node_maps[word.text]=word.text

        for word in doc.sentences[0].words:
            # self.f.node_attr.update(color='blue')
            self.f.node(node_maps[word.text])
            segs.append(node_maps[word.text])

        # self.f.node_attr.update(color='black')
        self.print_dependencies(doc.sentences[0], segs, node_maps)
        return self.f

class LangDialect(object):
    """
    >>> from sagas.nlu.corenlp_helper import LangDialect
    >>> LangDialect('ko').ana('나는 중국 출신이다.')
    """
    def __init__(self, lang, local_translit=False, outf=None):
        from sagas.nlu.translator import get_word_map
        from sagas.nlu.transliterations import translits
        # self.translits=Transliterations()
        self.lang=lang
        def viz(sents, trans_it=True):
            nlp=get_nlp(self.lang)
            doc = nlp(sents)
            cv=CoreNlpViz(shape='egg', size='8,5', fontsize=20)
            words=[word.text for sent in doc.sentences for word in sent.words]
            if trans_it:
                rs_trans=self.trans_to(sents, ['en'])
                if outf is not None:
                    for r in rs_trans:
                        outf(r)
                else:
                    print(*rs_trans, sep='\n')
                if self.lang in translits.available_langs():
                    if outf is not None:
                        outf('♡ '+translits.translit(sents, self.lang))
                    else:
                        print('♡', translits.translit(sents, self.lang))
                tr_map, tr_tab=get_word_map(self.lang, 'en', sents, 0, words, local_translit=local_translit)
                if outf is not None:
                    outf(' '.join(tr_tab))
            else:
                tr_map=None
            return cv.analyse_doc(doc, tr_map)

        self.ana=viz
        self.ana_en= lambda sents: self.ana(self.tra(sents))
        self.ana_s = lambda sents: self.ana(sents, trans_it=False)

    def tra(self, sents):
        from sagas.nlu.translator import translate
        r,_ = translate(sents, source='en', target=self.lang)
        print(r)
        return r

    def trans_to(self, sents, targets):
        from sagas.nlu.translator import translate
        rs=[]
        for target in targets:
            r,_ = translate(sents, source=self.lang, target=target)
            # print(r)
            rs.append(r)
        return rs

