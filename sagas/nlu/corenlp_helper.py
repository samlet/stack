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

langs={'zh':nlp_zh, 'en':nlp_en,
        'fr':nlp_fr, 'ja':nlp_ja,
        'it':nlp_it, 'pt':nlp_pt,
        'es':nlp_es, 'ru':nlp_ru,
        'de':nlp_de,
        'hi':lambda: load_model('hi', 'hi_hdtb')
       }

langs_models={}
def get_nlp(lang):
    if lang not in langs_models:
        langs_models[lang]=langs[lang]()
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
    def __init__(self):
        from graphviz import Digraph
        self.f = Digraph('deps', filename='deps.gv')
        self.f.attr(rankdir='LR', size='8,5')
        self.f.attr('node', shape='circle')

    def print_dependencies(self, doc, segs, node_maps, file=None):
        for dep_edge in doc.dependencies:
            print((dep_edge[2].text, dep_edge[0].index, dep_edge[1]), file=file)
            # head = int(dep_edge[0].index)
            # governor-id is index in words list + 1
            head = int(dep_edge[0].index)-1
            node_text=node_maps[dep_edge[2].text]
            self.f.edge(segs[head], node_text, label=dep_edge[1])
            # self.f.edge(dep_edge[2].text, segs[head], label=dep_edge[1])

    def analyse(self, sents, nlp, node_maps=None):
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
        doc = nlp(sents)
        print(*[f'text: {word.text+" "}\tlemma: {word.lemma}\tupos: {word.upos}\txpos: {word.xpos}' for sent in
                doc.sentences for word in sent.words], sep='\n')
        if node_maps is None:
            node_maps={}
            for word in doc.sentences[0].words:
                node_maps[word.text]=word.text

        for word in doc.sentences[0].words:
            self.f.node(node_maps[word.text])
            segs.append(node_maps[word.text])
        self.print_dependencies(doc.sentences[0], segs, node_maps)
        return self.f

if __name__ == '__main__':
    import fire
    fire.Fire(CoreNlp)

