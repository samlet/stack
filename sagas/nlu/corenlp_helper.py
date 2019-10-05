import stanfordnlp
import pandas as pd

model_dir='/pi/ai/corenlp'

def analyse(sents, nlp):
    doc = nlp(sents)
    print(*[f'text: {word.text+" "}\tlemma: {word.lemma}\tupos: {word.upos}\txpos: {word.xpos}' for sent in doc.sentences for word in sent.words], sep='\n')
    doc.sentences[0].print_dependencies()

def nlp_zh():
    return stanfordnlp.Pipeline(models_dir=model_dir,
                              lang='zh',
                              treebank='zh_gsd')

def nlp_ja():
    return stanfordnlp.Pipeline(models_dir=model_dir,
                              lang='ja',
                              treebank='ja_gsd')

def nlp_de():
    return stanfordnlp.Pipeline(models_dir=model_dir,
                              lang='de',
                              treebank='de_gsd')
def nlp_it():
    return stanfordnlp.Pipeline(models_dir=model_dir,
                              lang='it',
                              treebank='it_isdt')
def nlp_pt():
    return stanfordnlp.Pipeline(models_dir=model_dir,
                              lang='pt',
                              treebank='pt_bosque')
# es_ancora
def nlp_es():
    return stanfordnlp.Pipeline(models_dir=model_dir,
                              lang='es',
                              treebank='es_ancora')

# ru_syntagrus_models
def nlp_ru():
    return stanfordnlp.Pipeline(models_dir=model_dir,
                                lang='ru',
                                treebank='ru_syntagrus')

def nlp_fr():
    config = {
        'processors': 'tokenize,mwt,pos,lemma,depparse',  # Comma-separated list of processors to use
        'lang': 'fr',  # Language code for the language to build the Pipeline in
        'tokenize_model_path': model_dir + '/fr_gsd_models/fr_gsd_tokenizer.pt',
    # Processor-specific arguments are set with keys "{processor_name}_{argument_name}"
        'mwt_model_path': model_dir + '/fr_gsd_models/fr_gsd_mwt_expander.pt',
        'pos_model_path': model_dir + '/fr_gsd_models/fr_gsd_tagger.pt',
        'pos_pretrain_path': model_dir + '/fr_gsd_models/fr_gsd.pretrain.pt',
        'lemma_model_path': model_dir + '/fr_gsd_models/fr_gsd_lemmatizer.pt',
        'depparse_model_path': model_dir + '/fr_gsd_models/fr_gsd_parser.pt',
        'depparse_pretrain_path': model_dir + '/fr_gsd_models/fr_gsd.pretrain.pt'
    }
    nlp = stanfordnlp.Pipeline(**config)  # Initialize the pipeline using a configuration dict
    return nlp

def nlp_en():
    return stanfordnlp.Pipeline(models_dir=model_dir, treebank='en_ewt')

def nlp_en_common():
    return stanfordnlp.Pipeline(
        processors="tokenize,mwt,lemma,pos,depparse",
        models_dir=model_dir, treebank='en_ewt')

def load_model(lang,treebank):
    return stanfordnlp.Pipeline(models_dir=model_dir,
                                lang=lang,
                                treebank=treebank)

langs={ 'zh':nlp_zh, 'en':nlp_en,
        'fr':nlp_fr, 'ja':nlp_ja,
        'it':nlp_it, 'pt':nlp_pt,
        'es':nlp_es, 'ru':nlp_ru,
        'de':nlp_de,
        'hi':lambda: load_model('hi', 'hi_hdtb'),
        'ar':lambda: load_model('ar', 'ar_padt'),
        # Urdu(乌尔都语)
        'ur':lambda: load_model('ur', 'ur_udtb'),
        # Korean
        'ko':lambda: load_model('ko', 'ko_kaist'),
        # Vietnamese
        'vi':lambda: load_model('vi', 'vi_vtb'),
        # Persian
        'fa':lambda: load_model('fa', 'fa_seraji'),
        # Czech
        'cs':lambda: load_model('cs', 'cs_pdt'),
        # Slovak
        'sk':lambda: load_model('sk', 'sk_snk'),
        # Polish
        'pl':lambda: load_model('pl', 'pl_lfg'),
        # Turkish
        'tr':lambda: load_model('tr', 'tr_imst'),
        # Swedish
        'sv':lambda: load_model('sv', 'sv_talbanken'),
        # Norwegian	Bokmaal
        'no':lambda: load_model('no', 'no_bokmaal'),
        # Bulgarian (保加利亚语)
        'bg':lambda: load_model('bg', 'bg_btb'),
        # Croatian (克罗地亚语)
        'hr':lambda: load_model('hr', 'hr_set'),
        # Serbian (塞尔维亚语)
        'sr':lambda: load_model('sr', 'sr_set'),
        # Danish (丹麦语)
        'da':lambda: load_model('da', 'da_ddt'),
        # Dutch
        'nl':lambda: load_model('da', 'nl_alpino'),
        # Greek
        'el':lambda: load_model('el', 'el_gdt'),
        # Catalan (加泰罗尼亚语)
        'ca':lambda: load_model('ca', 'ca_ancora'),
        # Hungarian (匈牙利语)
        'hu':lambda: load_model('hu', 'hu_szeged'),
        # Irish (爱尔兰语)
        'ga':lambda: load_model('ga', 'ga_idt'),
       }

langs_models={}
def get_nlp(lang):
    if lang not in langs_models:
        if lang in langs:
            langs_models[lang]=langs[lang]()
        else:
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

class CoreNlp(object):
    def __init__(self):
        pass

    def parse(self, sents, lang='en'):
        """
        $ python -m sagas.nlu.corenlp_helper parse 'Barack Obama was born in Hawaii.' en
        $ parse 'Die weiße Fläche ist aus dem All sichtbar.' de
        $ parse '私は高校生です。' ja
        $ parse 'Yo tengo una casa en México.' es
        :param sents:
        :param lang:
        :return:
        """
        routine=langs[lang]
        analyse(sents, routine())

    def en(self, sents):
        """
        $ python -m sagas.nlu.corenlp_helper en 'Barack Obama was born in Hawaii.'
        :param sents:
        :return:
        """
        analyse(sents, nlp_en())

    def de(self, sents):
        """
        $ python -m sagas.nlu.corenlp_helper de 'Die weiße Fläche ist aus dem All sichtbar.'
        :param sents:
        :return:
        """
        analyse(sents, nlp_de())

    def ja(self, sents):
        """
        $ python -m sagas.nlu.corenlp_helper ja '私は高校生です。'
        :param sents:
        :return:
        """
        analyse(sents, nlp_ja())


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
        from sagas.nlu.google_translator import get_word_map
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
        from sagas.nlu.google_translator import translate
        r,_ = translate(sents, source='en', target=self.lang)
        print(r)
        return r

    def trans_to(self, sents, targets):
        from sagas.nlu.google_translator import translate
        rs=[]
        for target in targets:
            r,_ = translate(sents, source=self.lang, target=target)
            # print(r)
            rs.append(r)
        return rs

if __name__ == '__main__':
    import fire
    fire.Fire(CoreNlp)

