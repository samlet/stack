import stanfordnlp

from sagas.nlu.corenlp_helper import model_dir, get_nlp, load_model


def analyse(sents, nlp):
    doc = nlp(sents)
    print(*[f'text: {word.text+" "}\tlemma: {word.lemma}\tupos: {word.upos}\txpos: {word.xpos}' for sent in doc.sentences for word in sent.words], sep='\n')
    doc.sentences[0].print_dependencies()
    for word in doc.sentences[0].words:
        # ⊕ [Universal features](https://universaldependencies.org/u/feat/all.html)
        print(word.text, '--', word.feats)

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

class CoreNlp(object):
    def __init__(self):
        pass

    def parse(self, sents, lang='en'):
        """
        $ python -m sagas.nlu.corenlp_helper parse 'Barack Obama was born in Hawaii.' en
        $ python -m sagas.nlu.corenlp_helper parse 'Θα το θέλατε με ρύζι;' el

        $ parse 'Die weiße Fläche ist aus dem All sichtbar.' de
        $ parse '私は高校生です。' ja
        $ parse 'Yo tengo una casa en México.' es

        :param sents:
        :param lang:
        :return:
        """
        # routine=langs[lang]
        analyse(sents, get_nlp(lang))

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


if __name__ == '__main__':
    import fire
    fire.Fire(CoreNlp)

